"""Offline correctness/scale exercise, NOT Google or Claude latency measurement."""
import copy,json,sys,time,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import graph_cortex as g
def timed(fn,repeats=3):
 values=[]
 for _ in range(repeats):
  t=time.perf_counter();result=fn();values.append((time.perf_counter()-t)*1000)
 return {'median_ms':statistics.median(values),'range_ms':[min(values),max(values)]},result
def run(count):
 t=time.perf_counter();book=g.fixture(count);build=time.perf_counter()-t
 at,state=timed(lambda:g.audit(book));target=book['Nodes'][-1];start=book['Nodes'][3]['node_id']
 direct,_=timed(lambda:g.direct(book,target['node_id'],target['revision_id'],len(book['Nodes'])+1))
 search,found=timed(lambda:[r for r in book['Nodes'] if r['node_id']==target['node_id']]);assert found==[target]
 keyword,_=timed(lambda:[r for r in book['Nodes'] if r['kind']=='Knowledge' and 'Launch' in r['title']])
 one,one_result=timed(lambda:g.traverse(book,start,1));two,two_result=timed(lambda:g.traverse(book,start,2));assert len(two_result['node_ids'])>len(one_result['node_ids'])
 op=g.uid();n=g.node(op,g.uid(),'New synthetic learning');e=g.edge(op,n['node_id'],target['node_id'],'about','Explicit synthetic relationship');ev=g.event(op,n['node_id'],n['content'])
 t=time.perf_counter();g.commit(book,op,[('History',ev),('Nodes',n),('Edges',e)]);g.audit(book);add_ms=(time.perf_counter()-t)*1000
 prior=copy.deepcopy(target);op=g.uid();new=g.node(op,target['node_id'],prior['content']+' Revised with preserved reason.',bases=[prior['revision_id']],version=2)
 t=time.perf_counter();g.commit(book,op,[('History',g.event(op,target['node_id'],g.canonical(prior),'prior_state')),('History',g.event(op,target['node_id'],'Revision reason')),('Nodes',new)]);g.audit(book);revision_ms=(time.perf_counter()-t)*1000
 assert prior in book['Nodes'];assert book['Nodes'][-1]['content'].startswith(prior['content'])
 return {'initial_nodes':count,'initial_edges':count,'build_seconds':build,'offline_full_audit':at,'offline_direct_hint':direct,'offline_ID_linear_scan':search,'offline_keyword_scan':keyword,'offline_one_hop_including_full_audit':one,'offline_two_hops_including_full_audit':two,'offline_create_node_edge_verify_ms':add_ms,'offline_revision_verify_ms':revision_ms,'exact_integrity_pass':True,'google_calls':0,'claude_response_latency':None}
if __name__=='__main__':
 out={'environment':'local Python only; full in-memory materialization is test harness, NOT recommended runtime retrieval','results':[run(n) for n in [10,1000,10000]]}
 path=ROOT/'tests/GRAPH_SCALE_LOCAL.json';path.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
