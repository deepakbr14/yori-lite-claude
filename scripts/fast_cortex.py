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
def collect(rows):
    ops=defaultdict(dict);totals={}
    for raw in rows:
        r=normalize(raw);op,p,n=r[:3]
        if op in totals and totals[op]!=n:raise Invalid('operation size collision')
        totals[op]=n
        if p in ops[op] and ops[op][p]!=r:raise Invalid('same operation/part, different contents')
        ops[op][p]=r
    complete=[];pending={}
    for op,parts in ops.items():
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

def audit(rows,old=None):
    complete,pending=collect(rows);versions=legacy_records(old) if old is not None else {}
    for r in complete:
        key=rid(r)
        if key in versions:raise Invalid('legacy revision ID collision')
        versions[key]={'rid':key,'id':r[4] or key,'parents':r[5].split(',') if r[5] else [],'family':r[3] if r[3]!='REVISION' else None,'kind':r[6].removeprefix('!'),'subject':decode_literal(r[7]),'object':decode_literal(r[8]),'text':decode_literal(r[9]),'by':decode_literal(r[10]),'basis':BASIS[r[11]],'source':decode_literal(r[12]),'at':decode_literal(r[13]),'raw':r,'origin':'fast','status':'retired' if r[6].startswith('!') else 'active'}
    # Resolve revisions topologically, so branches and multi-parent reconciliation survive.
    resolved={k:v for k,v in versions.items() if not v['parents']};todo={k:v for k,v in versions.items() if v['parents']}
    while todo:
        ready=[k for k,v in todo.items() if all(p in resolved for p in v['parents'])]
        if not ready:raise Incomplete('missing/cyclic predecessor; dependent recall is incomplete')
        for k in ready:
            v=todo.pop(k);parents=[resolved[p] for p in v['parents']]
            if any(p['id']!=v['id'] for p in parents):raise Invalid('cross-entity predecessor')
            family=parents[0]['family']
            if any(p['family']!=family for p in parents) or v['family'] not in (None,family):raise Invalid('family change')
            v['family']=family;resolved[k]=v
    consumed={p for v in resolved.values() for p in v['parents']};heads=defaultdict(list)
    for k,v in resolved.items():
        if v['family']=='NODE' and v['object']:raise Invalid('node object')
        if k not in consumed:heads[v['id']].append(v)
    node_ids={v['id'] for v in resolved.values() if v['family']=='NODE'}
    for v in resolved.values():
        if v['family']=='EDGE' and (v['subject'] not in node_ids or v['object'] not in node_ids):raise Incomplete('edge endpoint missing')
    return {'versions':resolved,'heads':dict(heads),'pending':pending,'legacy_history':legacy.committed(old)['History'] if old is not None else []}

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

# ---- 0.4.2 fast confirmation: append_values + server-side op count (findReplace op->op) ----
NEW_OP=r'op[A-Za-z0-9]{8,40}'
def new_op_ok(op):
    """New writers use 'op' + letters/digits: never parsed as number/date/bool/formula when re-entered."""
    return bool(re.fullmatch(NEW_OP,op))
def count_request(op,sheet_id=0):
    """update_spreadsheet requests: identity find/replace of the op token, whole cells, whole Memory sheet.
    The reply's occurrencesChanged counts every stored row of this op, wherever it landed."""
    if not new_op_ok(op):raise Invalid('op token not safe for count')
    return [{'findReplace':{'find':op,'replacement':op,'sheetId':sheet_id,'matchEntireCell':True,'matchCase':True}}]
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
