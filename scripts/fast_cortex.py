"""Offline FAST protocol verifier and legacy adapter; NOT a runtime prerequisite.
Claude writes short arrays directly. No hashes, network, credentials or backend.
"""
import copy,json,re
from collections import defaultdict
import graph_cortex as legacy
HEADER='op part total type id parents kind subject object text by basis source at'.split()
BASIS={'S':'explicit_statement','I':'inference','D':'decision','E':'external_evidence','M':'mixed','U':'unknown'}
class Invalid(ValueError):pass
class Incomplete(Invalid):pass

def normalize(row):
    if not isinstance(row,list) or len(row)>14:raise Invalid('row shape')
    row=row+['']*(14-len(row))
    if len(row)<3 or not isinstance(row[0],str) or not re.fullmatch(r'[A-Za-z0-9_-]{8,128}',row[0]):raise Invalid('operation ID')
    for i in (1,2):
        # get_values returns formatted strings ("1"); appended JSON numbers stay numbers.
        if isinstance(row[i],str) and re.fullmatch(r'[1-9][0-9]{0,2}',row[i]):row[i]=int(row[i])
        if type(row[i]) not in (int,float) or int(row[i])!=row[i] or row[i]<1:raise Invalid('part/total')
        row[i]=int(row[i])
    if row[1]>row[2] or row[2]>100:raise Invalid('part bounds')
    if any(not isinstance(v,str) for i,v in enumerate(row) if i not in (1,2)):raise Invalid('nonliteral field')
    if row[3] not in ('NODE','EDGE','REVISION') or row[11] not in BASIS:raise Invalid('type/basis')
    if not row[6] or not row[9] or not row[10] or not row[12]:raise Invalid('missing meaning/attribution')
    bases=row[5].split(',') if row[5] else []
    if len(bases)!=len(set(bases)) or any(not b or b.strip()!=b for b in bases):raise Invalid('parents')
    if row[3]=='REVISION':
        if not row[4] or not bases:raise Invalid('revision identity/parents')
    elif row[4] or bases:raise Invalid('root ID is derived; no parents')
    if row[3]=='EDGE' and (not row[7] or not row[8]):raise Invalid('edge endpoints')
    if row[3]=='NODE' and row[8]:raise Invalid('node has no object')
    return row

def encode_literal(value):
    return '~'+value if value and value[0] in "=+-@'~" else value
def decode_literal(value):
    return value[1:] if len(value)>1 and value[0]=='~' and value[1] in "=+-@'~" else value
# Every free-text column carries the ~ codec; decoding is uniform so old rows and new rows agree.
TEXT_COLUMNS=(7,8,9,10,12,13)  # subject object text by source at
def wire_cell(value):
    """Value sent through append_values (USER_ENTERED, no RAW option exposed).
    A leading apostrophe is Sheets' literal-text marker: stripped on storage, it
    forces an exact string even in rows beyond the formatted grid. Numbers pass."""
    if not isinstance(value,str):return value
    return "'"+value if value else value
def wire_row(row):
    """Intended row -> exact append_values cells: ~ codec on text columns, apostrophe on every nonempty string."""
    out=list(row)
    for i in TEXT_COLUMNS:
        if i<len(out) and isinstance(out[i],str):out[i]=encode_literal(out[i])
    return [wire_cell(v) for v in out]
def stored_row(row):
    """Cells as get_values should return them after a correct wire_row append."""
    out=list(row)
    for i in TEXT_COLUMNS:
        if i<len(out) and isinstance(out[i],str):out[i]=encode_literal(out[i])
    while out and out[-1]=='':out.pop()
    return [str(v) if not isinstance(v,str) else v for v in out]

def rid(row):return f'{row[0]}:{row[1]}'
def collect(rows,quarantine=None):
    """quarantine=None: raise on conflicts (strict). A dict: record conflicting ops there and leave them out."""
    ops=defaultdict(dict);totals={};bad=set()
    for raw in rows:
        try:r=normalize(raw)
        except Invalid as e:
            if quarantine is None:raise
            quarantine[str(raw[0] if raw else '?')]=f'malformed row: {e}';continue
        op,p,n=r[:3]
        if op in totals and totals[op]!=n:
            if quarantine is None:raise Invalid('operation size collision')
            bad.add(op);quarantine[op]='operation size collision';continue
        totals[op]=n
        if p in ops[op] and ops[op][p]!=r:
            if quarantine is None:raise Invalid('same operation/part, different contents')
            bad.add(op);quarantine[op]='same operation/part, different contents';continue
        ops[op][p]=r
    complete=[];pending={}
    for op,parts in ops.items():
        if op in bad:continue
        missing=sorted(set(range(1,totals[op]+1))-parts.keys())
        if missing:pending[op]=missing
        else:complete.extend(parts[p] for p in sorted(parts))
    return complete,pending

def legacy_records(book):
    """Read schema-1 commits without changing/copying any saved source rows."""
    visible=legacy.committed(book);legacy.audit(book);out={}
    for tab,family,key in [('Nodes','NODE','node_id'),('Edges','EDGE','edge_id')]:
        for r in visible[tab]:
            out[r['revision_id']]={'rid':r['revision_id'],'id':r[key],'parents':json.loads(r['base_revision_ids'] or '[]'),'family':family,'kind':r.get('kind',r.get('relation')),'subject':r.get('subject',r.get('from_node_id','')),'object':r.get('to_node_id',''),'text':r.get('content',r.get('evidence','')),'by':r['contributor'],'basis':r['attribution'],'source':r.get('source',r.get('evidence','')),'at':r.get('updated_at',r.get('created_at','')),'raw':copy.deepcopy(r),'origin':'legacy','status':r['status']}
    return out

def audit(rows,old=None,strict=True):
    """strict=False: a bad operation is set aside in 'quarantine' with its reason instead of failing the whole read."""
    q=None if strict else {}
    complete,pending=collect(rows,q);versions=legacy_records(old) if old is not None else {}
    for r in complete:
        key=rid(r)
        if key in versions:raise Invalid('legacy revision ID collision')
        versions[key]={'rid':key,'id':r[4] or key,'parents':r[5].split(',') if r[5] else [],'family':r[3] if r[3]!='REVISION' else None,'kind':r[6].removeprefix('!'),'subject':decode_literal(r[7]),'object':decode_literal(r[8]),'text':decode_literal(r[9]),'by':decode_literal(r[10]),'basis':BASIS[r[11]],'source':decode_literal(r[12]),'at':decode_literal(r[13]),'raw':r,'origin':'fast','status':'retired' if r[6].startswith('!') else 'active'}
    # Resolve revisions topologically, so branches and multi-parent reconciliation survive.
    resolved={k:v for k,v in versions.items() if not v['parents']};todo={k:v for k,v in versions.items() if v['parents']}
    while todo:
        ready=[k for k,v in todo.items() if all(p in resolved for p in v['parents'])]
        if not ready:
            if strict:raise Incomplete('missing/cyclic predecessor; dependent recall is incomplete')
            for k in todo:q[k]='missing or cyclic predecessor'
            break
        for k in ready:
            v=todo.pop(k);parents=[resolved[p] for p in v['parents']]
            # Repair a known writer slip: a revision of a revision that names the previous REVISION ID as its
            # entity. The parent pins the entity unambiguously, so read it as that entity and flag it.
            if v['id'] in resolved and resolved[v['id']]['id']!=v['id'] and v['id'] in v['parents']:
                v['repaired']=f"id named revision {v['id']}; read as entity {resolved[v['id']]['id']}";v['id']=resolved[v['id']]['id']
            try:
                if any(p['id']!=v['id'] for p in parents):raise Invalid('cross-entity predecessor')
                family=parents[0]['family']
                if any(p['family']!=family for p in parents) or v['family'] not in (None,family):raise Invalid('family change')
            except Invalid as e:
                if strict:raise
                q[k]=str(e);continue
            v['family']=family;resolved[k]=v
    consumed={p for v in resolved.values() for p in v['parents']};heads=defaultdict(list)
    for k,v in resolved.items():
        if v['family']=='NODE' and v['object']:raise Invalid('node object')
        if k not in consumed:heads[v['id']].append(v)
    node_ids={v['id'] for v in resolved.values() if v['family']=='NODE'}
    for v in list(resolved.values()):
        if v['family']=='EDGE' and (v['subject'] not in node_ids or v['object'] not in node_ids):
            if strict:raise Incomplete('edge endpoint missing')
            q[v['rid']]='edge endpoint missing'
            if v in heads.get(v['id'],[]):heads[v['id']].remove(v)
    out={'versions':resolved,'heads':{k:h for k,h in heads.items() if h},'pending':pending,'legacy_history':legacy.committed(old)['History'] if old is not None else []}
    if not strict:out['quarantine']=q
    return out

def recover(expected,observed,coverage=False):
    expected=[normalize(r) for r in expected];full,pending=collect(expected)
    if pending or len({r[0] for r in full})!=1:raise Invalid('expected one complete operation')
    plan={rid(r):r for r in full};op=full[0][0];found={}
    for raw in observed:
        r=normalize(raw)
        if r[0]!=op:continue
        if rid(r) not in plan or plan[rid(r)]!=r:raise Invalid('operation collision; never retry altered content')
        found[rid(r)]=r
    missing=[r for r in full if rid(r) not in found]
    if missing and not coverage:raise Incomplete('window cannot prove absence')
    return {'state':'verified' if not missing else 'retry_original_rows','rows':missing}

# ---- op-count tool (recovery: complete coverage of an op's rows); 0.4.2 used it as default, reverted in 0.4.3 ----
NEW_OP=r'op[A-Za-z0-9]{8,40}'
def new_op_ok(op):
    """New writers use 'op' + letters/digits: never parsed as number/date/bool/formula when re-entered."""
    return bool(re.fullmatch(NEW_OP,op))
def count_request(op,sheet_id=0):
    """update_spreadsheet requests: identity find/replace of the op token, whole cells, column A of Memory.
    The reply's occurrencesChanged counts every stored row of this op, wherever it landed."""
    if not new_op_ok(op):raise Invalid('op token not safe for count')
    # Column A only: live test showed sheet scope also counts the token in other columns (overcount can mask a missing row).
    return [{'findReplace':{'find':op,'replacement':op,'range':{'sheetId':sheet_id,'startColumnIndex':0,'endColumnIndex':1},'matchEntireCell':True,'matchCase':True}}]
def count_from_reply(reply):
    """update_spreadsheet reply -> int. Live: zero matches return findReplace {} with no field."""
    fr=((reply or {}).get('replies') or [{}])[0].get('findReplace')
    return None if fr is None else int(fr.get('occurrencesChanged',0))
def sent_cells(wire_rows):return sum(len(r) for r in wire_rows)
def confirm(wire_rows,receipt,count,recounted=False):
    """Decide a save from the append receipt and the op count. Never uses updatedRange.
    Returns verified | recount | pending | check_duplicates | uncertain."""
    n=len(wire_rows)
    u=(receipt or {}).get('updates') or {}
    ok=(receipt or {}).get('status')=='success' and u.get('updatedRows')==n and u.get('updatedCells')==sent_cells(wire_rows)
    if count is None:return 'uncertain'
    if ok and count==n:return 'verified'
    if ok and count==0 and not recounted:return 'recount'  # count may have run before the append landed
    if count>n:return 'check_duplicates'               # earlier retry or token collision: read and compare the op's rows
    if not ok and count==n:return 'check_duplicates'   # rows exist but this receipt did not prove they are ours
    return 'pending' if count<n else 'uncertain'

# ---- 0.4.3 default verification: same-message tail-window read-back, matched by op and exact content ----
def window_range(last_end,size=20):
    """Rows after the last row this chat has seen (a lower bound), never a receipt position."""
    return f'Memory!A{last_end+1}:N{last_end+size}'
def locate(window,wire_rows,size=20):
    """Find the intended op in a get_values window. Returns (state, last_row_offset).
    verified | not_seen (window not full: read may have preceded the append; read once more) |
    beyond (window full of other rows: read the next window) | pending (some parts) | conflict."""
    want=[expected_read(r) for r in wire_rows];op=want[0][0]
    by_part={int(r[1]):r for r in want};seen={};last=None
    for i,row in enumerate(window):
        if row and row[0]==op:
            p=int(row[1]) if str(row[1]).isdigit() else None
            if p not in by_part or row!=by_part[p]:return 'conflict',i
            seen[p]=row;last=i
    if len(seen)==len(by_part):return 'verified',last
    if seen:return 'pending',last
    return ('beyond' if len(window)>=size and all(window) else 'not_seen'),None
def expected_read(wire):
    """What get_values returns for a correctly appended wire row: apostrophe consumed, numbers as text, trailing blanks dropped."""
    out=[str(c) if not isinstance(c,str) else c for c in unwire(wire)]
    while out and out[-1]=='':out.pop()
    return out
def unwire(row):return [c[1:] if isinstance(c,str) and c.startswith("'") else c for c in row]

# ---- 0.4.4 default: one append per save, receipt gate now, content audit at the next read ----
def receipt_ok(wire_rows,receipt):
    """Clean append receipt: success, row and cell counts equal what was sent, landed in Memory column A.
    Row numbers in updatedRange are never used (simultaneous writers were told wrong rows)."""
    u=(receipt or {}).get('updates') or {}
    return bool((receipt or {}).get('status')=='success' and u.get('updatedRows')==len(wire_rows)
                and u.get('updatedCells')==sent_cells(wire_rows) and str(u.get('updatedRange','')).startswith('Memory!A'))
def after_append(wire_rows,receipt,first_save_in_chat):
    """'done' (written, count confirmed; audit at next read) or 'read_back' (verify by content now)."""
    return 'read_back' if first_save_in_chat or not receipt_ok(wire_rows,receipt) else 'done'
def audit_saved(read_rows,saved_ops):
    """Deferred audit: read_rows = Memory rows read from E+1; saved_ops = list of wire-row lists kept from this chat.
    Returns {op: state} using the same exact-content matching as the read-back."""
    return {unwire(rows[0])[0]:locate(read_rows,rows,size=len(read_rows)+1)[0] for rows in saved_ops}

# ---- 0.4.5 Yori's own side: views, open threads, interests as Self rows ----
def self_side(state):
    """Active Self heads grouped for chat start: identity/other, views, open threads, interests.
    A thread closed by a !Self revision (and with no concurrent active head) is not open."""
    out={'identity':[],'views':[],'open':[],'interests':[]}
    for heads in state['heads'].values():
        active=[v for v in heads if v['kind']=='Self' and v['family']=='NODE' and v['status']=='active']
        for v in active:
            s=v['subject']
            key='views' if s.startswith('self/view/') else 'open' if s.startswith('self/open/') else 'interests' if s.startswith('self/interest/') else 'identity'
            out[key].append(v)
    return out

# ---- 0.4.6 Library: books in Drive, coverage in Memory ----
def library_books(state):
    """Active book rows: {subject: {'files':[ids], 'read':str, 'notes':id|None, 'text':str}} parsed from the row text."""
    out={}
    for heads in state['heads'].values():
        for v in heads:
            if v['family']=='NODE' and v['status']=='active' and v['subject'].startswith('library/book/'):
                t=v['text'];g=lambda k:(re.search(k+r':\s*(.*?)(?:\.\s+(?:Files|Read|Notes):|\.?$)',t) or [None,''])[1].strip()
                out[v['subject']]={'files':[x.strip() for x in g('Files').split(',') if x.strip()],'read':g('Read'),'notes':g('Notes') or None,'text':t}
    return out
def library_folder(state):
    for heads in state['heads'].values():
        for v in heads:
            if v['family']=='NODE' and v['status']=='active' and v['subject']=='library':
                m=re.search(r'Library folder:\s*([A-Za-z0-9_-]+)',v['text'])
                if m:return m[1]
    return None
def unread_files(state,drive_files):
    """drive_files: [{'id','title'}] listed from the Library folder. Returns files not named in any book row,
    skipping Yori's own notes documents."""
    known={f for b in library_books(state).values() for f in b['files']}|{b['notes'] for b in library_books(state).values() if b['notes']}
    return [d for d in drive_files if d['id'] not in known and not d['title'].startswith('Yori notes')]

# ---- 0.4.7 summary tabs: Current (cache of what is true now) and Self (Yori's own page) ----
CURRENT_HEADER=['kind','subject','entity','row','text']
def head_rows(rows):
    """Map revision ID -> Memory sheet row number (header is row 1)."""
    return {f'{r[0]}:{r[1]}':i+2 for i,r in enumerate(rows) if len(r)>1}
def short(text,limit=160):
    t=' '.join(str(text).split());return t if len(t)<=limit else t[:limit-1].rstrip()+'…'
def build_current(rows,through=None):
    """Rows for the Current tab from Memory data rows (row 2 onward). Active People/Knowledge/Concept NODE heads only:
    no Self (that is Yori's own page), no edges, no retired items. Text is shortened: a summary, never the record."""
    st=audit(rows,strict=False);where=head_rows(rows);through=through or len(rows)+1
    order={'People':0,'Knowledge':1,'Concept':2}
    out=[]
    for ent,heads in st['heads'].items():
        for v in heads:
            if v['family']=='NODE' and v['status']=='active' and v['kind'] in order:
                out.append([v['kind'],v['subject'],ent,str(where.get(v['rid'],'')),short(v['text'],120)+(' [concurrent versions]' if len(heads)>1 else '')])
    out.sort(key=lambda r:(order[r[0]],r[1],int(r[3] or 0)))
    title=[f'Current: summary built by Yori from Memory rows 2-{through}. Memory is the record; this tab can be rebuilt.','','','','']
    return [title,CURRENT_HEADER]+out
def read_current(lines):
    """Current tab lines (after title and header) -> {entity: line}. Append-only: the last line for an entity wins;
    kind 'retired' removes it."""
    out={}
    for r in lines:
        r=list(r)+['']*(5-len(r))
        if not r[2]:continue
        if r[0]=='retired':out.pop(r[2],None)
        else:out[r[2]]=r
    return out
def current_delta(tail_rows,first_row):
    """Lines to append to Current for Memory rows after its title N. tail_rows start at sheet row first_row.
    Revisions of an entity give a fresh line for that entity; a retirement gives a 'retired' line."""
    out=[];order={'People','Knowledge','Concept'}
    for i,raw in enumerate(tail_rows):
        r=list(raw)+['']*(14-len(raw))
        if r[3] not in ('NODE','REVISION'):continue
        kind=r[6].removeprefix('!')
        if kind not in order:continue
        ent=r[4] or f'{r[0]}:{r[1]}'
        if r[6].startswith('!'):out.append(['retired',decode_literal(r[7]),ent,str(first_row+i),short(decode_literal(r[9]),120)])
        else:out.append([kind,decode_literal(r[7]),ent,str(first_row+i),short(decode_literal(r[9]),120)])
    return out
def through_row(title_cell):
    m=re.search(r'rows 2-(\d+)',title_cell or '');return int(m[1]) if m else None
def self_material(rows):
    """What Yori consolidates into her Self page: active Self heads grouped, with Memory rows."""
    st=audit(rows,strict=False);where=head_rows(rows);side=self_side(st)
    return {k:[(v['subject'],v['entity'] if 'entity' in v else v['id'],where.get(v['rid']),v['text']) for v in vs] for k,vs in side.items()}

class Index:
    """Offline model of in-chat index + tail refresh, NOT a hosted/persisted index."""
    def __init__(self,rows,old=None):self.rows=list(rows);self.old=old;self.rebuild()
    def rebuild(self):
        self.state=audit(self.rows,self.old);self.topics=defaultdict(set);self.links=defaultdict(set)
        for v in self.state['versions'].values():
            self.topics[v['subject']].add(v['id'])
        for key,heads in self.state['heads'].items():
            for v in heads:
                self.topics[v['subject']].add(key)
                if v['family']=='EDGE' and v['status']=='active':
                    self.links[v['subject']].add(key);self.links[v['object']].add(key)
    def refresh(self,tail):self.rows.extend(tail);self.rebuild()
    def by_id(self,key):return self.state['heads'].get(key,[])
    def topic(self,key):return [v for entity in self.topics[key] for v in self.by_id(entity)]
    def neighbors(self,key):
        """Active traversal: only active EDGE heads. A retired concurrent head is history, never a live link."""
        return [v for entity in self.links[key] for v in self.by_id(entity) if v['family']=='EDGE' and v['status']=='active']
    def contested(self,entity):
        """True when an entity's concurrent heads disagree on retirement; recall must disclose it."""
        return len({v['status'] for v in self.by_id(entity)})>1
    def history(self,key):
        """Every head of every edge touching key, retired included, for explicit history display."""
        return [v for entity,heads in self.state['heads'].items() for v in heads if v['family']=='EDGE' and key in (v['subject'],v['object'])]

def fixture(count=10):
    rows=[['fixture0',1,1,'NODE','','','People','participant/A','','Alex (synthetic).','Alex','S','disposable fixture','']]
    for n in range(count-1):
        op=f'fixture{n+1:08d}';rows.extend([
            [op,1,2,'NODE','','','Knowledge',f'topic/{n}','','Synthetic fact '+str(n),'Alex','S','disposable fixture',''],
            [op,2,2,'EDGE','','','about',op+':1','fixture0:1','Alex stated this fact.','Alex','S','disposable fixture','']])
    return rows
