"""Offline fixture/migration/audit utility. No network, credentials or plugin runtime.

Claude executes the Skills protocol with its own exposed connectors. This utility
does not prove Claude behavior or provide a backend. All output is a staging plan.
"""
import argparse, copy, hashlib, json, uuid
from pathlib import Path

HEADERS = {
 'Nodes': 'node_id revision_id operation_id kind title content subject contributor attribution source created_at updated_at event_time base_revision_ids version status'.split(),
 'Edges': 'edge_id revision_id operation_id from_node_id to_node_id relation strength evidence contributor attribution created_at base_revision_ids version status'.split(),
 'History': 'event_id operation_id event_type entity_id content contributor attribution source recorded_at base_revision_ids manifest'.split(),
 'Directory': 'hint_id node_id revision_id row_number operation_id verified_at'.split(),
 'Metadata': 'record_id key value recorded_at'.split(),
}
KEYS = {'Nodes':'revision_id', 'Edges':'revision_id', 'History':'event_id'}
ATTRIBUTIONS = {'explicit_statement','external_evidence','inference','decision','mixed','unknown'}
TIME = '2026-01-15T15:00:00Z'  # Synthetic fixture time only, never a live clock.
class IntegrityError(ValueError): pass
def uid(): return str(uuid.uuid4())
def canonical(value): return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
def digest(value): return hashlib.sha256(canonical(value).encode()).hexdigest()
def empty(): return {k:[] for k in HEADERS}
def row(tab, **kw):
    unknown = set(kw)-set(HEADERS[tab])
    if unknown: raise IntegrityError(f'unknown columns: {unknown}')
    return {k:kw.get(k,'') for k in HEADERS[tab]}
def event(op, entity, content, kind='contribution', contributor='Synthetic Yori', attribution='decision', source='Synthetic fixture', bases=(), event_id=None, recorded_at=TIME):
    return row('History',event_id=event_id or uid(),operation_id=op,event_type=kind,entity_id=entity,content=content,contributor=contributor,attribution=attribution,source=source,recorded_at=recorded_at,base_revision_ids=canonical(list(bases)))
def node(op, node_id, content, kind='Knowledge', title='Synthetic topic', contributor='Synthetic Yori', attribution='decision', bases=(), version=1, source='Synthetic fixture', revision_id=None, created_at=TIME, updated_at=TIME, event_time=''):
    return row('Nodes',node_id=node_id,revision_id=revision_id or uid(),operation_id=op,kind=kind,title=title,content=content,subject=title,contributor=contributor,attribution=attribution,source=source,created_at=created_at,updated_at=updated_at,event_time=event_time,base_revision_ids=canonical(list(bases)),version=version,status='active')
def edge(op, start, end, relation, evidence, edge_id=None):
    return row('Edges',edge_id=edge_id or uid(),revision_id=uid(),operation_id=op,from_node_id=start,to_node_id=end,relation=relation,strength='',evidence=evidence,contributor='Synthetic harness',attribution='external_evidence',created_at=TIME,base_revision_ids='[]',version=1,status='active')
def commit(book, op, records, recorded_at=TIME):
    manifest=[]
    for tab, record in records:
        if tab not in KEYS or record['operation_id']!=op: raise IntegrityError('operation scope')
        book[tab].append(copy.deepcopy(record))
        manifest.append({'tab':tab,'row_id':record[KEYS[tab]],'sha256':digest(record)})
    c=event(op,'','Verified operation manifest','commit',contributor='Synthetic harness',attribution='external_evidence',recorded_at=recorded_at)
    c['manifest']=canonical(manifest);book['History'].append(c)
    return c
def _list(text):
    try: value=json.loads(text or '[]')
    except (ValueError,TypeError) as e: raise IntegrityError('invalid JSON list') from e
    if not isinstance(value,list): raise IntegrityError('not a list')
    return value
def committed(book):
    """Audit physical duplicates and manifests; never choose a corrupt winner."""
    maps={t:{} for t in KEYS}
    for tab,key in KEYS.items():
        for r in book[tab]:
            if set(r)!=set(HEADERS[tab]) or not r[key] or not r['operation_id']: raise IntegrityError('shape or ID')
            for field,value in r.items():
                if field=='version':
                    if type(value) is not int or value<1:raise IntegrityError('invalid version type')
                elif not isinstance(value,str):raise IntegrityError('nonliteral field type')
            if r['attribution'] not in ATTRIBUTIONS:raise IntegrityError('unknown attribution category')
            if tab in ('Nodes','Edges') and r['status'] not in ('active','retired'):raise IntegrityError('invalid status')
            if tab=='Nodes' and (not r['node_id'] or not r['content'] or not r['kind']):raise IntegrityError('incomplete node')
            if tab=='Edges' and (not r['edge_id'] or not r['relation'] or not r['evidence']):raise IntegrityError('incomplete edge')
            if r[key] in maps[tab] and maps[tab][r[key]]!=r: raise IntegrityError('same ID, different payload')
            maps[tab][r[key]]=r
    visible={t:{} for t in KEYS}; operations={}
    for c in maps['History'].values():
        if c['event_type']!='commit': continue
        manifest=_list(c['manifest']); op=c['operation_id']
        if op in operations and operations[op]!=manifest: raise IntegrityError('conflicting commits')
        operations[op]=manifest
        members=[]
        for m in manifest:
            if not isinstance(m,dict) or m.get('tab') not in KEYS: raise IntegrityError('bad manifest')
            r=maps[m['tab']].get(m.get('row_id'))
            if r is None: raise IntegrityError('missing manifest member')
            if r['operation_id']!=op or (m['tab']=='History' and r['event_type']=='commit'): raise IntegrityError('manifest operation mismatch')
            if ('sha256' in m)==('payload' in m): raise IntegrityError('one verification form required')
            if 'sha256' in m and digest(r)!=m['sha256']: raise IntegrityError('digest mismatch')
            if 'payload' in m and r!=m['payload']: raise IntegrityError('payload mismatch')
            members.append((m['tab'],r))
        if not members: raise IntegrityError('empty commit')
        for tab,r in members: visible[tab][r[KEYS[tab]]]=r
    return {t:list(rs.values()) for t,rs in visible.items()}
def heads(records, entity_key):
    versions={r['revision_id']:r for r in records}; consumed=set();children={r:[] for r in versions};degrees={}
    for rev,r in versions.items():
        bases=_list(r['base_revision_ids'])
        if len(bases)!=len(set(bases)):raise IntegrityError('duplicate predecessor')
        degrees[rev]=len(bases)
        for base in bases:
            if base not in versions:raise IntegrityError('missing predecessor')
            if versions[base][entity_key]!=r[entity_key]:raise IntegrityError('cross-entity predecessor')
            consumed.add(base);children[base].append(rev)
    ready=[r for r,d in degrees.items() if d==0];visited=0
    while ready:
        rev=ready.pop();visited+=1
        for child in children[rev]:
            degrees[child]-=1
            if degrees[child]==0:ready.append(child)
    if visited!=len(versions):raise IntegrityError('revision cycle')
    result={}
    for rev,r in versions.items():
        if rev not in consumed: result.setdefault(r[entity_key],[]).append(r)
    return result
def audit(book):
    visible=committed(book); ns=heads(visible['Nodes'],'node_id'); es=heads(visible['Edges'],'edge_id')
    for e in visible['Edges']:
        if e['from_node_id'] not in ns or e['to_node_id'] not in ns: raise IntegrityError('dangling endpoint')
    return {'nodes':ns,'edges':es,'history':visible['History']}
def direct(book,node_id,revision_id,physical_row):
    rows=book['Nodes'];i=physical_row-2
    if 0<=i<len(rows) and rows[i]['node_id']==node_id and rows[i]['revision_id']==revision_id:return rows[i]
    found=[r for r in rows if r['node_id']==node_id and r['revision_id']==revision_id]
    if not found:raise IntegrityError('stale pointer, ID unavailable')
    if any(r!=found[0] for r in found):raise IntegrityError('ambiguous pointer recovery')
    return found[0]  # Still requires committed-head resolution before current recall.
def traverse(book,start,hops=1):
    if hops not in (1,2):raise ValueError('only one or two hops')
    state=audit(book)
    if start not in state['nodes']:raise IntegrityError('unknown node')
    frontier={start};seen={start}; paths=[]
    for _ in range(hops):
        next_frontier=set()
        for revisions in state['edges'].values():
            for e in revisions:
                if e['status']!='active':continue
                a,b=e['from_node_id'],e['to_node_id']
                for origin,target in ((a,b),(b,a)):
                    if origin in frontier:
                        paths.append((origin,e['edge_id'],target))
                        if target not in seen:next_frontier.add(target)
        seen.update(next_frontier);frontier=next_frontier
    return {'node_ids':sorted(seen),'paths':paths}
def fixture(count=10):
    if count<10:raise ValueError('fixture requires >=10 nodes')
    book=empty(); ids=[uid() for _ in range(count)]
    content=[
      ('Self','Favorite color','Amber: the light people read and think by, and the kind of attention I want to bring. Original reason; no steadiness claim.'),
      ('People','Alex','Alex explicitly prefers blue. Pronouns unknown. Synthetic participant A.'),
      ('People','Sam','Sam requests accessibility review before launch. Pronouns unknown. Synthetic participant B.'),
      ('Knowledge','Launch decision','Explicit synthetic joint decision: delay launch until accessibility review finishes. Earlier positions differed; no other motives established.'),
      ('Concept','Accessibility review','Review required before launch in the synthetic joint decision.'),
      ('Knowledge','Alex proposal','Alex proposed Friday to meet the pilot window. This was a proposal, not the final decision.'),
      ('Knowledge','Sam position','Sam opposed launching before the accessibility review. Do not infer fear or other motives.'),
      ('Knowledge','Project','Synthetic Aurora project.'),
      ('Concept','Reading light','Reading and thinking light is the stated analogy behind amber.'),
      ('Knowledge','Decision evidence','Synthetic Alex and Sam explicitly agreed to delay. This fixture asserts agreement, not a real conversation.')]
    for i,nid in enumerate(ids):
        kind,title,body=content[i] if i<10 else ('Knowledge',f'Synthetic node {i}',f'Synthetic complete memory {i}; no real person data.')
        op=uid();n=node(op,nid,body,kind,title,attribution='decision' if kind=='Self' else 'external_evidence')
        ev=event(op,nid,body,attribution=n['attribution']);commit(book,op,[('History',ev),('Nodes',n)])
    links=[(0,8,'explained_by'),(3,4,'depends_on'),(3,9,'supported_by'),(9,5,'records_revision_of'),(9,6,'records_position'),(5,1,'attributed_to'),(6,2,'attributed_to'),(3,7,'about'),(4,7,'about'),(8,0,'explains')]
    # Synthetic scale edges are explicitly generated fixture relations, not learned claims.
    links += [(i,i-1,'synthetic_predecessor') for i in range(10,count)]
    for a,b,relation in links:
        op=uid();e=edge(op,ids[a],ids[b],relation,'Explicit synthetic fixture relationship; not inferred from user memories.')
        commit(book,op,[('History',event(op,e['edge_id'],e['evidence'],attribution='external_evidence')),('Edges',e)])
    for i,n in enumerate(book['Nodes'],2):book['Directory'].append(row('Directory',hint_id=uid(),node_id=n['node_id'],revision_id=n['revision_id'],row_number=i,operation_id=n['operation_id'],verified_at=TIME))
    for k,v in [('cortex_id',uid()),('schema_version','1'),('storage_format','sheets-graph-v1'),('fixture','synthetic only'),('created_at',TIME)]:book['Metadata'].append(row('Metadata',record_id=uid(),key=k,value=v,recorded_at=TIME))
    return book
def migrate(snapshot):
    """Convert a complete connector-exported Docs snapshot. Never writes Drive.

    Input content must preserve all relevant tabs, sections, reasons and attribution.
    Raw provider response is retained in source when supplied. No inferred edges.
    """
    if snapshot.get('complete') is not True or not snapshot.get('cortex_folder_id'):raise IntegrityError('complete scoped export required')
    docs=snapshot.get('documents',[])
    if not docs:raise IntegrityError('empty export')
    book=empty();seen=set();namespace=uuid.UUID('b6a4f87b-3495-4095-bdba-a42151bbccac')
    for d in docs:
        for key in ['id','kind','title','content','source_revision']:
            if not isinstance(d.get(key),str) or not d[key]:raise IntegrityError(f'missing {key}')
        if d['id'] in seen:raise IntegrityError('duplicate source ID')
        seen.add(d['id'])
        if d.get('complete') is not True or d.get('verified_in_scope') is not True:raise IntegrityError('unverified source')
        if d['kind'] not in ['Self','People','Knowledge','History']:raise IntegrityError('unknown source kind; retain for review')
        op=str(uuid.uuid5(namespace,canonical(d)));rid=str(uuid.uuid5(namespace,op+':version'))
        source=canonical({'source_id':d['id'],'source_revision':d['source_revision'],'source_folder_id':snapshot['cortex_folder_id'],'url':d.get('url',''),'raw_document':d.get('raw_document',None)})
        evidence=event(op,d['id'],d['content'],'legacy_history' if d['kind']=='History' else 'migration_evidence',contributor=d.get('contributor','unknown — preserved in source text'),attribution=d.get('attribution','unknown'),source=source,event_id=d['id'] if d['kind']=='History' else str(uuid.uuid5(namespace,op+':evidence')),recorded_at=snapshot.get('exported_at',''))
        records=[('History',evidence)]
        if d['kind']!='History':
            n=node(op,d['id'],d['content'],d['kind'],d['title'],contributor=evidence['contributor'],attribution=evidence['attribution'],source=source,revision_id=rid,created_at=d.get('created_at',''),updated_at=d.get('updated_at',''),event_time=d.get('event_time',''))
            records.append(('Nodes',n))
        c=commit(book,op,records,recorded_at=snapshot.get('exported_at',''))
        c['event_id']=str(uuid.uuid5(namespace,op+':commit'))
    # Migration does not guess predecessor links, person merges or semantic edges.
    for i,n in enumerate(book['Nodes'],2):book['Directory'].append(row('Directory',hint_id=str(uuid.uuid5(namespace,n['revision_id']+':hint')),node_id=n['node_id'],revision_id=n['revision_id'],row_number=i,operation_id=n['operation_id'],verified_at=''))
    for k,v in [('cortex_id',str(uuid.uuid5(namespace,snapshot['cortex_folder_id']+digest(snapshot)))),('schema_version','1'),('storage_format','sheets-graph-v1'),('created_at',snapshot.get('exported_at','')),('migration_source_folder',snapshot['cortex_folder_id']),('migration_snapshot_sha256',digest(snapshot)),('migration_status','staged-unverified')]:book['Metadata'].append(row('Metadata',record_id=str(uuid.uuid5(namespace,k+v)),key=k,value=v,recorded_at=snapshot.get('exported_at','')))
    # Avoid promising a truncated import; fail before any remote operation.
    for tab,records in book.items():
        for r in records:
            for value in r.values():
                if isinstance(value,str) and len(value)>40000:raise IntegrityError('conservative 40k cell staging limit; source preserved, manual review needed')
    audit(book);return book
def main():
    p=argparse.ArgumentParser(description=__doc__);s=p.add_subparsers(dest='command',required=True)
    f=s.add_parser('fixture');f.add_argument('--nodes',type=int,default=10);f.add_argument('--output',type=Path,required=True)
    m=s.add_parser('migrate');m.add_argument('snapshot',type=Path);m.add_argument('--output',type=Path,required=True)
    a=s.add_parser('audit');a.add_argument('book',type=Path)
    args=p.parse_args()
    if args.command=='audit':
        state=audit(json.loads(args.book.read_text()));print(json.dumps({'nodes':len(state['nodes']),'edges':len(state['edges']),'conflicted_nodes':sum(len(x)>1 for x in state['nodes'].values())}));return
    book=fixture(args.nodes) if args.command=='fixture' else migrate(json.loads(args.snapshot.read_text()))
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(book,ensure_ascii=False,indent=2)+'\n');print(args.output)
if __name__=='__main__':main()
