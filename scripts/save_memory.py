"""Prepare one small attributed memory using a fixed helper, never generated Bash.

Offline only. This does NOT invoke Claude's connector. Pass --json a compact intent
object; retain the plan file to reuse exact IDs after an uncertain tool response.
Only tool arguments are printed, never a second copy of records or a Bash script.
"""
import argparse,json
from datetime import datetime,timezone
from pathlib import Path
import graph_cortex as g
import batch_memory as b

def prepare(intent):
    allowed={'sheet_ids','spreadsheet_id','kind','title','content','contributor','attribution','source','reason','subject','event_time','node_id','bases','version','created_at','edge'}
    if set(intent)-allowed:raise g.IntegrityError('unknown intent fields')
    for k in ('spreadsheet_id','kind','title','content','contributor','attribution','source'):
        if not isinstance(intent.get(k),str) or not intent[k]:raise g.IntegrityError('missing '+k)
    if intent['kind'] not in ('Self','People','Knowledge','Concept'):raise g.IntegrityError('kind')
    if intent['attribution'] not in g.ATTRIBUTIONS:raise g.IntegrityError('attribution')
    bases=intent.get('bases',[])
    if not isinstance(bases,list) or any(not isinstance(x,str) or not x for x in bases) or len(set(bases))!=len(bases):raise g.IntegrityError('bases')
    if bases and (not intent.get('node_id') or not intent.get('reason') or not intent.get('created_at') or type(intent.get('version')) is not int or intent['version']<2):raise g.IntegrityError('revision needs verified node, bases, original time, version and reason')
    if not bases and (intent.get('node_id') or intent.get('version',1)!=1):raise g.IntegrityError('existing node requires verified predecessors')
    now=datetime.now(timezone.utc).isoformat(timespec='seconds');op=g.uid();nid=intent.get('node_id') or g.uid()
    n=g.node(op,nid,intent['content'],kind=intent['kind'],title=intent['title'],contributor=intent['contributor'],attribution=intent['attribution'],source=intent['source'],bases=bases,version=intent.get('version',1),created_at=intent.get('created_at',now),updated_at=now,event_time=intent.get('event_time',''))
    n['subject']=intent.get('subject','')
    # History references the immutable revision rather than copying its content.
    h=g.event(op,nid,intent.get('reason',''),contributor=intent['contributor'],attribution=intent['attribution'],source=n['revision_id'],bases=bases,recorded_at=now)
    records=[('Nodes',n),('History',h)]
    if intent.get('edge'):
        e=intent['edge']
        if set(e)!={'to','relation','evidence','contributor','attribution'} or any(not isinstance(v,str) or not v for v in e.values()):raise g.IntegrityError('edge requires explicit endpoint, relation, evidence and author')
        if e['attribution'] not in g.ATTRIBUTIONS:raise g.IntegrityError('edge attribution')
        edge=g.edge(op,nid,e['to'],e['relation'],e['evidence']);edge.update(contributor=e['contributor'],attribution=e['attribution'],created_at=now)
        records.append(('Edges',edge))
    plan=b.prepare(records,intent['sheet_ids'],now)
    plan['tool_arguments']={'spreadsheet_id':intent['spreadsheet_id'],'requests':plan['requests']}
    return plan

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--json',required=True);p.add_argument('--plan',required=True,type=Path);a=p.parse_args()
    intent=json.loads(a.json)
    if a.plan.exists():
        saved=json.loads(a.plan.read_text())
        if saved['intent']!=intent:raise g.IntegrityError('plan path already belongs to another intent')
        plan=saved['plan']
    else:
        plan=prepare(intent)
        # Exclusive creation prevents accidental replacement of recovery evidence.
        with a.plan.open('x') as f:json.dump({'intent':intent,'plan':plan},f,separators=(',',':'),ensure_ascii=False)
    print(json.dumps(plan['tool_arguments'],separators=(',',':'),ensure_ascii=False))
if __name__=='__main__':main()
