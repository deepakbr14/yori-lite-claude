"""Offline tests of packaged preparation/recovery, not Claude capability evidence."""
import copy,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import graph_cortex as g
import batch_memory as b

class BatchMemoryTests(unittest.TestCase):
 def setUp(self):
  self.book=g.fixture(10);self.original=copy.deepcopy(self.book);self.ids={'Nodes':11,'Edges':22,'History':33}
 def fact(self,number=5,base=None):
  op=g.uid();person=self.book['Nodes'][1]['node_id'];nid=base['node_id'] if base else g.uid()
  n=g.node(op,nid,f'Alex explicitly says their favorite number is {number}.',kind='People',title='Favorite number',contributor=person,attribution='explicit_statement',bases=[base['revision_id']] if base else [],version=2 if base else 1)
  n['subject']=person+'/favorite_number';h=g.event(op,nid,f'Alex stated {number}; no unstated motive.','contribution',person,'explicit_statement',bases=[base['revision_id']] if base else [])
  return [('Nodes',n),('History',h)]
 def apply(self,plan,book=None):
  target=self.book if book is None else book
  for tab,r in plan['records']:target[tab].append(copy.deepcopy(r))
 def test_one_batch_contains_payload_and_commit_no_directory(self):
  p=b.prepare(self.fact(),self.ids,g.TIME);self.assertEqual(len(p['requests']),2)
  self.assertTrue(all('appendCells' in r for r in p['requests']));self.assertEqual(p['records'][-1][1]['event_type'],'commit')
  self.apply(p);self.assertTrue(b.verify(p,self.book));g.audit(self.book)
  self.assertEqual(self.book['Directory'],self.original['Directory'])
 def test_fact_does_not_rewrite_identity_profile(self):
  p=b.prepare(self.fact(),self.ids,g.TIME);self.apply(p)
  self.assertEqual(self.book['Nodes'][:10],self.original['Nodes']);self.assertLess(len(p['records'][0][1]['content']),256)
 def test_revision_preserves_prior_row_without_duplicate_snapshot(self):
  first=b.prepare(self.fact(),self.ids,g.TIME);self.apply(first);old=copy.deepcopy(first['records'][0][1])
  second=b.prepare(self.fact(7,old),self.ids,g.TIME);self.apply(second);state=g.audit(self.book)
  self.assertIn(old,self.book['Nodes']);self.assertEqual(len(state['nodes'][old['node_id']]),1)
  self.assertFalse(any(r.get('event_type')=='prior_state' for _,r in second['records']))
 def test_supported_edge_in_same_batch(self):
  rs=self.fact();e=g.edge(rs[0][1]['operation_id'],rs[0][1]['node_id'],self.book['Nodes'][1]['node_id'],'about','The stated preference belongs to this participant.');rs.append(('Edges',e))
  p=b.prepare(rs,self.ids,g.TIME);self.apply(p);self.assertEqual(len(g.audit(self.book)['edges']),11)
 def test_response_lost_recovery_has_no_second_write(self):
  p=b.prepare(self.fact(),self.ids,g.TIME);self.apply(p);self.assertEqual(b.recover(p,self.book)['records'],[])
 def test_incomplete_window_never_means_absent(self):
  p=b.prepare(self.fact(),self.ids,g.TIME)
  with self.assertRaises(b.NeedsLookup):b.recover(p,{},complete=False)
 def test_partial_payload_resume_retains_same_ids(self):
  p=b.prepare(self.fact(),self.ids,g.TIME);obs=g.empty();t,r=p['records'][0];obs[t].append(r)
  recovery=b.recover(p,obs,complete=True);self.assertEqual(recovery['records'],p['records'][1:])
 def test_commit_with_missing_payload_is_corruption_not_repair(self):
  p=b.prepare(self.fact(),self.ids,g.TIME);obs=g.empty();t,r=p['records'][-1];obs[t].append(r)
  with self.assertRaises(g.IntegrityError):b.recover(p,obs,complete=True)
 def test_identical_physical_duplicates_one_logical_fact(self):
  p=b.prepare(self.fact(),self.ids,g.TIME);self.apply(p);self.apply(p);self.assertTrue(b.verify(p,self.book));self.assertEqual(len(g.audit(self.book)['nodes']),11)
 def test_different_payload_same_ID_rejected(self):
  p=b.prepare(self.fact(),self.ids,g.TIME);self.apply(p);self.book['Nodes'][-1]['content']='wrong'
  with self.assertRaises(g.IntegrityError):b.recover(p,self.book,complete=True)
 def test_conflicting_revisions_preserve_both(self):
  initial=b.prepare(self.fact(),self.ids,g.TIME);self.apply(initial);base=initial['records'][0][1]
  a=b.prepare(self.fact(7,base),self.ids,g.TIME);c=b.prepare(self.fact(9,base),self.ids,g.TIME);self.apply(a);self.apply(c)
  state=g.audit(self.book);self.assertEqual(len(state['nodes'][base['node_id']]),2);self.assertIn(base,self.book['Nodes'])
 def test_ordered_keys_are_not_silently_misaddressed(self):
  rs=self.fact();rs[0]=(rs[0][0],dict(reversed(list(rs[0][1].items()))))
  p=b.prepare(rs,self.ids,g.TIME);values=p['requests'][0]['appendCells']['rows'][0]['values']
  self.assertEqual(values[0]['userEnteredValue']['stringValue'],rs[0][1]['node_id'])
if __name__=='__main__':unittest.main()
