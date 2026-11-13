import copy,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import fast_cortex as f,graph_cortex as g
class FastTests(unittest.TestCase):
 def setUp(self):self.rows=f.fixture(2)
 def rev(self,value='7',op='revision0001',base='fixture00000001:1'):
  return [op,1,1,'REVISION','fixture00000001:1',base,'Knowledge','topic/0','',value+'; explicit correction.','Alex','S','test conversation','']
 def test_node_edge(self):
  a=f.audit(self.rows);self.assertEqual(len(a['heads']),3)
 def test_partial_operation_invisible(self):
  a=f.audit(self.rows[:2]);self.assertEqual(len(a['heads']),1);self.assertTrue(a['pending'])
 def test_complete_restores_visibility(self):
  a=f.audit(self.rows[:2]+self.rows[2:]);self.assertFalse(a['pending'])
 def test_identical_retry_one_memory(self):self.assertEqual(len(f.audit(self.rows+self.rows)['heads']),3)
 def test_conflicting_duplicate_rejected(self):
  bad=copy.deepcopy(self.rows[-1]);bad[9]='different'
  with self.assertRaises(f.Invalid):f.audit(self.rows+[bad])
 def test_recovery_missing_only(self):self.assertEqual(f.recover(self.rows[1:],self.rows[:2],True)['rows'],self.rows[2:])
 def test_recovery_not_proven_absent(self):
  with self.assertRaises(f.Incomplete):f.recover(self.rows[1:],self.rows[:2])
 def test_lost_ack_no_write(self):self.assertEqual(f.recover(self.rows[1:],self.rows)['rows'],[])
 def test_revision_keeps_original(self):
  a=f.audit(self.rows+[self.rev()]);self.assertEqual(len(a['versions']),4);self.assertEqual(len(a['heads']['fixture00000001:1']),1)
 def test_concurrent_branches(self):self.assertEqual(len(f.audit(self.rows+[self.rev(),self.rev('9','revision0002')])['heads']['fixture00000001:1']),2)
 def test_reconciliation(self):
  r=self.rev('8','revision0003','revision0001:1,revision0002:1');a=f.audit(self.rows+[self.rev(),self.rev('9','revision0002'),r]);self.assertEqual(len(a['heads']['fixture00000001:1']),1)
 def test_third_unseen_branch(self):
  r=self.rev('8','revision0003','revision0001:1,revision0002:1');a=f.audit(self.rows+[self.rev(),self.rev('9','revision0002'),r,self.rev('11','revision0004')]);self.assertEqual(len(a['heads']['fixture00000001:1']),2)
 def test_missing_parent(self):
  with self.assertRaises(f.Incomplete):f.audit(self.rows+[self.rev(base='missing:1')])
 def test_cross_entity(self):
  with self.assertRaises(f.Invalid):f.audit(self.rows+[self.rev(base='fixture0:1')])
 def test_cycles(self):
  with self.assertRaises(f.Incomplete):f.audit(self.rows+[self.rev(base='revision0001:1')])
 def test_missing_endpoint(self):
  r=copy.deepcopy(self.rows);r[-1][8]='absent'
  with self.assertRaises(f.Incomplete):f.audit(r)
 def test_changed_count(self):
  r=copy.deepcopy(self.rows);r[-1][2]=3
  with self.assertRaises(f.Invalid):f.audit(r)
 def test_bad_slot(self):
  r=copy.deepcopy(self.rows);r[-1][1]=4
  with self.assertRaises(f.Invalid):f.audit(r)
 def test_unknown_attribution(self):
  r=copy.deepcopy(self.rows);r[-1][11]='madeup'
  with self.assertRaises(f.Invalid):f.audit(r)
 def test_missing_source(self):
  r=copy.deepcopy(self.rows);r[-1][12]=''
  with self.assertRaises(f.Invalid):f.audit(r)
 def test_trimmed_empty_time(self):self.assertEqual(f.audit([r[:-1] for r in self.rows]),f.audit(self.rows))
 def test_partial_row_rejected(self):
  with self.assertRaises(f.Invalid):f.audit([self.rows[0][:8]])
 def test_index_reads(self):
  i=f.Index(self.rows);self.assertTrue(i.topic('topic/0'));self.assertTrue(i.neighbors('fixture0:1'));self.assertTrue(i.by_id('fixture0:1'))
 def test_incremental_refresh(self):
  i=f.Index(self.rows);i.refresh([self.rev()]);self.assertTrue(i.by_id('fixture00000001:1')[0]['text'].startswith('7'))
 def test_legacy_read_preserves_every_version_and_history(self):
  b=g.fixture(10);old=copy.deepcopy(b);state=f.audit([],b)
  self.assertEqual(b,old);self.assertEqual(len(state['versions']),20);self.assertEqual(len(state['legacy_history']),20)
 def test_revision_of_legacy_identity(self):
  b=g.fixture(10);n=b['Nodes'][0];r=['legacyrev1',1,1,'REVISION',n['node_id'],n['revision_id'],'Self',n['subject'],'','Amber; original reason retained, new thought separately attributed.','Yori','D','test correction','']
  a=f.audit([r],b);self.assertEqual(len(a['heads'][n['node_id']]),1);self.assertIn(n['revision_id'],a['versions'])
 def test_late_legacy_branch_preserved(self):
  b=g.fixture(10);n=b['Nodes'][0];r=['legacyrev1',1,1,'REVISION',n['node_id'],n['revision_id'],'Self',n['subject'],'','Amber; revised reason.','Yori','D','test correction',''];op=g.uid();late=g.node(op,n['node_id'],'Red',kind='Self',bases=[n['revision_id']],version=2);g.commit(b,op,[('Nodes',late)])
  self.assertEqual(len(f.audit([r],b)['heads'][n['node_id']]),2)
 def test_old_data_corruption_detected(self):
  b=g.fixture(10);b['Nodes'][0]['content']='changed'
  with self.assertRaises(g.IntegrityError):f.audit([],b)
 def test_source_fidelity_literal(self):
  r=copy.deepcopy(self.rows);r[1][9]='=1+1 — a literal quote, not a formula';self.assertEqual(f.audit(r)['versions']['fixture00000001:1']['text'],r[1][9])
 def test_more_than_one_op_plan_refused(self):
  with self.assertRaises(f.Invalid):f.recover(self.rows,self.rows)

class FastSafetyTests(unittest.TestCase):
 def test_literal_codec(self):
  for value in ['=1+1','+12','-bad','@something',"'quote",'~original','Blue.','']:
   self.assertEqual(f.decode_literal(f.encode_literal(value)),value)
 def test_old_topic_still_resolves_current(self):
  rows=f.fixture(2);r=['changedtopic',1,1,'REVISION','fixture00000001:1','fixture00000001:1','Knowledge','new/topic','','Updated meaning; topic renamed.','Alex','S','test',''];i=f.Index(rows+[r]);self.assertEqual(i.topic('topic/0')[0]['subject'],'new/topic')
 def test_new_and_dual_configs(self):
  sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'));from check_package import validate
  root=Path(__file__).resolve().parents[1];schema=json.loads((root/'schemas/config.schema.json').read_text());c=json.loads((root/'templates/config.fast.example.json').read_text());validate(c,schema)
  c['active_cortex']['legacy_graph_spreadsheet_id']='original';validate(c,schema)
  c['storage_format']='sheets-graph-v1'
  with self.assertRaises(ValueError):validate(c,schema)
 def test_fast_missing_workbook_rejected(self):
  sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'));from check_package import validate
  root=Path(__file__).resolve().parents[1];schema=json.loads((root/'schemas/config.schema.json').read_text());c=json.loads((root/'templates/config.fast.example.json').read_text());del c['active_cortex']['google_sheets_spreadsheet_id']
  with self.assertRaises(ValueError):validate(c,schema)

class RetirementTests(unittest.TestCase):
 def test_legacy_retirement_preserved(self):
  b=g.fixture(10);n=b['Nodes'][0];op=g.uid();r=g.node(op,n['node_id'],n['content'],kind=n['kind'],bases=[n['revision_id']],version=2);r['status']='retired';g.commit(b,op,[('Nodes',r)])
  self.assertEqual(f.audit([],b)['heads'][n['node_id']][0]['status'],'retired')
 def test_retired_edge_history_not_active_traversal(self):
  rows=f.fixture(2);rows.append(['retireedge',1,1,'REVISION','fixture00000001:2','fixture00000001:2','!about','fixture00000001:1','fixture0:1','Retired: relation no longer holds.','Yori','D','test',''])
  i=f.Index(rows);self.assertEqual(i.neighbors('fixture0:1'),[]);self.assertEqual(i.by_id('fixture00000001:2')[0]['status'],'retired')
