"""Tests the shipped offline protocol utility, NOT Claude or a live connector."""
import copy,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import graph_cortex as g

class GraphTests(unittest.TestCase):
 def setUp(self):self.b=g.fixture(10)
 def test_fixture_references_and_two_hops(self):
  a=g.audit(self.b);self.assertEqual(len(a['nodes']),10);self.assertEqual(len(a['edges']),10)
  ids=[r['node_id'] for r in self.b['Nodes']]
  one=g.traverse(self.b,ids[3],1);two=g.traverse(self.b,ids[3],2)
  self.assertNotIn(ids[5],one['node_ids']);self.assertIn(ids[5],two['node_ids']);self.assertIn(ids[6],two['node_ids'])
 def test_stale_pointer_cannot_return_different_node(self):
  r=self.b['Nodes'][0];self.b['Nodes'].reverse();self.assertEqual(g.direct(self.b,r['node_id'],r['revision_id'],2),r)
 def test_exact_retry_is_one_logical_record(self):
  self.b['Nodes']+=copy.deepcopy(self.b['Nodes']);self.b['History']+=copy.deepcopy(self.b['History']);self.assertEqual(len(g.audit(self.b)['nodes']),10)
 def test_mismatching_duplicate_rejected(self):
  r=copy.deepcopy(self.b['Nodes'][0]);r['content']='different';self.b['Nodes'].append(r)
  with self.assertRaises(g.IntegrityError):g.audit(self.b)
 def test_uncommitted_node_not_current(self):
  n=g.node(g.uid(),g.uid(),'pending');self.b['Nodes'].append(n);self.assertNotIn(n['node_id'],g.audit(self.b)['nodes'])
 def test_partial_committed_batch_not_accepted(self):
  self.b['Nodes'].pop()
  with self.assertRaises(g.IntegrityError):g.audit(self.b)
 def test_committed_history_mutation_detected(self):
  self.b['History'][0]['content']='technical repair'
  with self.assertRaises(g.IntegrityError):g.audit(self.b)
 def revision(self,base,text):
  op=g.uid();n=g.node(op,base['node_id'],text,kind=base['kind'],bases=[base['revision_id']],version=2)
  snap=g.event(op,base['node_id'],g.canonical(base),'prior_state',bases=[base['revision_id']])
  contribution=g.event(op,base['node_id'],text);g.commit(self.b,op,[('History',snap),('History',contribution),('Nodes',n)]);return n
 def test_both_writers_and_explicit_reconciliation(self):
  old=copy.deepcopy(self.b['Nodes'][0]);a=self.revision(old,'A reason');b=self.revision(old,'B reason')
  self.assertEqual(len(g.audit(self.b)['nodes'][old['node_id']]),2)
  op=g.uid();merged=g.node(op,old['node_id'],'A and B retained; reconciliation explained',bases=[a['revision_id'],b['revision_id']],version=3)
  g.commit(self.b,op,[('Nodes',merged),('History',g.event(op,old['node_id'],g.canonical([a,b]),'prior_state'))]);self.assertEqual(len(g.audit(self.b)['nodes'][old['node_id']]),1)
  self.assertEqual(self.b['Nodes'][0],old)
  self.revision(old,'Unseen third writer');self.assertEqual(len(g.audit(self.b)['nodes'][old['node_id']]),2)
 def test_newest_timestamp_not_winner(self):
  old=self.b['Nodes'][0];self.revision(old,'one');other=self.revision(old,'two');other['updated_at']='2099-01-01T00:00:00Z'
  self.assertEqual(len(g.audit(self.b)['nodes'][old['node_id']]),2)
 def test_cross_entity_predecessor_rejected(self):
  n=g.node(g.uid(),g.uid(),'bad',bases=[self.b['Nodes'][0]['revision_id']]);g.commit(self.b,n['operation_id'],[('Nodes',n)])
  with self.assertRaises(g.IntegrityError):g.audit(self.b)
 def test_dangling_edge_rejected(self):
  e=g.edge(g.uid(),self.b['Nodes'][0]['node_id'],g.uid(),'about','unknown endpoint');g.commit(self.b,e['operation_id'],[('Edges',e)])
  with self.assertRaises(g.IntegrityError):g.audit(self.b)
 def test_revision_cycle_rejected(self):
  op=g.uid();nid=g.uid();a=g.node(op,nid,'A');b=g.node(op,nid,'B',bases=[a['revision_id']]);a['base_revision_ids']=g.canonical([b['revision_id']]);g.commit(self.b,op,[('Nodes',a),('Nodes',b)])
  with self.assertRaises(g.IntegrityError):g.audit(self.b)
 def test_version_counter_does_not_accept_boolean(self):
  n=g.node(g.uid(),g.uid(),'bad counter',version=True);g.commit(self.b,n['operation_id'],[('Nodes',n)])
  with self.assertRaises(g.IntegrityError):g.audit(self.b)
 def test_explicit_payload_manifest_without_hash(self):
  c=next(h for h in self.b['History'] if h['event_type']=='commit');m=json.loads(c['manifest'])
  for item in m:
   item.pop('sha256');item['payload']=next(r for r in self.b[item['tab']] if r[g.KEYS[item['tab']]]==item['row_id'])
  c['manifest']=g.canonical(m);self.assertEqual(len(g.audit(self.b)['nodes']),10)
 def test_fresh_reader_retains_self_and_history(self):
  restored=json.loads(json.dumps(self.b));a=g.audit(restored);self.assertIn('read and think',next(iter(a['nodes'].values()))[0]['content']);self.assertEqual(a,g.audit(self.b))
 def snapshot(self):return {'complete':True,'cortex_folder_id':'source-folder','exported_at':'2026-11-11T00:00:00Z','documents':[{'id':'original-self-id','kind':'Self','title':'Color','content':'Amber.\nOriginal reason, unknown motives, source context.','source_revision':'r1','complete':True,'verified_in_scope':True},{'id':'original-history-id','kind':'History','title':'Earlier evidence','content':'Person suggested red; motive unknown.','source_revision':'r2','complete':True,'verified_in_scope':True}]}
 def test_migration_exact_idempotent_no_fabricated_edges(self):
  s=self.snapshot();original=copy.deepcopy(s);a=g.migrate(s);b=g.migrate(s);self.assertEqual(a,b);self.assertEqual(s,original)
  self.assertEqual(a['Nodes'][0]['node_id'],'original-self-id');self.assertEqual(a['Nodes'][0]['content'],s['documents'][0]['content']);self.assertEqual(a['Edges'],[]);self.assertIn('original-history-id',[h['event_id'] for h in a['History']])
 def test_partial_migration_rejected(self):
  s=self.snapshot();s['documents'][0]['complete']=False
  with self.assertRaises(g.IntegrityError):g.migrate(s)
 def test_oversized_source_not_truncated(self):
  s=self.snapshot();s['documents'][0]['content']='x'*40001
  with self.assertRaises(g.IntegrityError):g.migrate(s)
  self.assertEqual(len(s['documents'][0]['content']),40001)
 def test_graph_config_requires_workbook_and_schema(self):
  r=Path(__file__).resolve().parents[1];sys.path.insert(0,str(r/'tools'))
  from check_package import validate
  schema=json.loads((r/'schemas/config.schema.json').read_text());good=json.loads((r/'templates/config.graph.example.json').read_text());validate(good,schema)
  for path in ['cortex_schema_version','google_sheets_spreadsheet_id']:
   bad=copy.deepcopy(good)
   if path=='cortex_schema_version':del bad[path]
   else:del bad['active_cortex'][path]
   with self.assertRaises(ValueError):validate(bad,schema)
if __name__=='__main__':unittest.main()
