"""Prepare/verify small schema-1 atomic append operations. No network/auth/backend.

Use only after the actual connector's atomic-batch capability is established.
Preparation includes a commit marker in the SAME batch; format remains 0.3.0-readable.
Caller supplies already scoped relevant context, genuine generated IDs and sheet IDs.
"""
import argparse,copy,json
from pathlib import Path
import graph_cortex as g

class NeedsLookup(g.IntegrityError): pass
def prepare(records,sheet_ids,recorded_at,commit_id=None):
    if not records:raise g.IntegrityError('empty operation')
    records=copy.deepcopy(records);ops={r['operation_id'] for _,r in records}
    if len(ops)!=1:raise g.IntegrityError('mixed operation IDs')
    if any(t not in g.KEYS or (t=='History' and r['event_type']=='commit') for t,r in records):raise g.IntegrityError('payload scope')
    book=g.empty();op=next(iter(ops));marker=g.commit(book,op,records,recorded_at=recorded_at)
    if commit_id:marker['event_id']=commit_id
    # The marker is bookkeeping, not a second contribution. Preserve only required
    # fields; evidence and recorded time live in the referenced contribution.
    for field in ('content','contributor','source','recorded_at','base_revision_ids'):
        marker[field]=''
    marker['attribution']='unknown'
    # Validate full payload shape/manifests without pretending external references were read here.
    g.committed(book)
    all_records=records+[('History',marker)]
    seen=set()
    for tab,r in all_records:
        key=(tab,r[g.KEYS[tab]])
        if key in seen:raise g.IntegrityError('duplicate planned row ID')
        seen.add(key)
    def cells(record,tab):
        values=[record[k] for k in g.HEADERS[tab]]
        while values and values[-1]=='':values.pop()
        # Interior blanks preserve positional columns; trailing blanks are omitted.
        return {'values':[{} if v=='' else {'userEnteredValue':
                {'numberValue':v} if type(v) is int else {'stringValue':v}}
                for v in values]}
    requests=[]
    # Same-tab contributions and final marker share one appendCells request.
    # No formatting, response grid echo, repeated full payload or Directory write.
    for tab in ['Nodes','Edges','History']:
        rows=[r for t,r in all_records if t==tab]
        if rows:
            if tab not in sheet_ids or type(sheet_ids[tab]) is not int:
                raise g.IntegrityError('verified numeric sheetId required')
            requests.append({'appendCells':{'sheetId':sheet_ids[tab],
                'rows':[cells(r,tab) for r in rows],'fields':'userEnteredValue'}})
    return {'operation_id':op,'records':all_records,'requests':requests}
def verify(plan,observed):
    for tab,expected in plan['records']:
        key=g.KEYS[tab];matches=[r for r in observed.get(tab,[]) if r.get(key)==expected[key]]
        if any(r!=expected for r in matches):raise g.IntegrityError('same row ID has different contents')
        if not matches:raise NeedsLookup('expected row outside verification coverage')
    return True
def recover(plan,observed,complete=False):
    try:verify(plan,observed);return {'state':'already_committed','records':[]}
    except NeedsLookup:pass
    # Conflicting payloads are detected even if an earlier expected record is missing.
    missing=[];present=[]
    for tab,expected in plan['records']:
        key=g.KEYS[tab];matches=[r for r in observed.get(tab,[]) if r.get(key)==expected[key]]
        if any(r!=expected for r in matches):raise g.IntegrityError('conflicting retry payload')
        (present if matches else missing).append((tab,expected))
    if not complete:raise NeedsLookup('absence is not established; expand scoped lookup')
    if any(t=='History' and r['event_type']=='commit' for t,r in present):raise g.IntegrityError('committed operation has missing payload; investigate, do not repair silently')
    return {'state':'resume_original_ids','records':missing}
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input',type=Path);p.add_argument('--output',required=True,type=Path);a=p.parse_args()
    d=json.loads(a.input.read_text());result=prepare(d['records'],d['sheet_ids'],d.get('recorded_at',''),d.get('commit_id'))
    a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(a.output)
if __name__=='__main__':main()
