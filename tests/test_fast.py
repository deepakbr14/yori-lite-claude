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

class CorrectnessFixes041(unittest.TestCase):
 """Regressions for the 0.4.1 correctness fixes (handoff findings 1-2, live Sheets literal finding)."""
 def edge_rev(self,op,kind):
  return [op,1,1,'REVISION','fixture00000001:2','fixture00000001:2',kind,'fixture00000001:1','fixture0:1',kind+' by concurrent writer.','Yori','D','test','']
 def test_concurrent_active_and_retired_edge_heads(self):
  rows=f.fixture(2)+[self.edge_rev('activeedge1','about'),self.edge_rev('retireedge1','!about')]
  i=f.Index(rows);n=i.neighbors('fixture0:1')
  self.assertEqual([v['status'] for v in n],['active'])
  self.assertTrue(i.contested('fixture00000001:2'))
  self.assertEqual(sorted(v['status'] for v in i.history('fixture0:1')),['active','retired'])
 def test_only_retired_heads_no_neighbors_but_history(self):
  rows=f.fixture(2)+[self.edge_rev('retireedge1','!about')];i=f.Index(rows)
  self.assertEqual(i.neighbors('fixture00000001:1'),[]);self.assertFalse(i.contested('fixture00000001:2'));self.assertEqual(len(i.history('fixture0:1')),1)
 def test_codec_decodes_every_text_column(self):
  rows=f.fixture(2);r=rows[1]
  r[7]='~~topic';r[10]='~@handle';r[12]='~=source';r[13]="~'2026"
  v=f.audit(rows)['versions']['fixture00000001:1']
  self.assertEqual((v['subject'],v['by'],v['source'],v['at']),('~topic','@handle','=source',"'2026"))
 def test_unencoded_existing_strings_unchanged(self):
  rows=f.fixture(2);rows[1][7]='~plain/topic';self.assertEqual(f.audit(rows)['versions']['fixture00000001:1']['subject'],'~plain/topic')
 def test_get_values_string_numbers_accepted(self):
  native=f.fixture(2);read=[f.stored_row(r) for r in native]
  self.assertTrue(all(isinstance(r[1],str) for r in read));self.assertEqual(f.audit(read)['heads'],f.audit(native)['heads'])
 def test_bad_string_counts_rejected(self):
  for bad in ('0','01','1.0',' 1','x','101'):
   r=copy.deepcopy(f.fixture(2));r[1][2]=bad
   with self.assertRaises(f.Invalid):f.audit(r)

class SheetsLiteralLive(unittest.TestCase):
 """Grounded in tests/SHEETS_LITERAL_LIVE.json: real append_values/get_values results."""
 @classmethod
 def setUpClass(cls):cls.e=json.loads((Path(__file__).parent/'SHEETS_LITERAL_LIVE.json').read_text())
 def test_wire_cells_match_live_sent(self):
  # Live run sent "'" for the empty value; wire_cell sends "". Both were stored as an empty cell.
  self.assertEqual([f.wire_cell(f.encode_literal(v)) or "'" for v in self.e['intended']],self.e['sent_wire'])
 def test_live_storage_exact_and_decodes(self):
  for want,stored in zip(self.e['intended'],self.e['stored_apostrophe_codec']):
   self.assertEqual(f.decode_literal(stored),want)
 def test_raw_sending_was_corrupted(self):
  bad=[v for v,s in zip(self.e['intended'],self.e['stored_raw_beyond_grid']) if v!=s]
  for v in ('=1+1','+abc','007','1e3','(5)','=',"'"):self.assertIn(v,bad)
 def test_wire_row_shape(self):
  row=['opWire0001',1,2,'NODE','','','Knowledge','007','','=1+1 is not a formula','@me','S','(5) 3/4 TRUE','2026-11-14']
  w=f.wire_row(row)
  self.assertEqual(w[1:3],[1,2])
  self.assertTrue(all(c=='' or c.startswith("'") for c in w if isinstance(c,str)))
  # Live behaviour: Sheets strips exactly one leading apostrophe and stores the rest as a string.
  stored=[c[1:] if isinstance(c,str) and c.startswith("'") else (str(c) if not isinstance(c,str) else c) for c in w]
  self.assertEqual(stored,f.stored_row(row)+['']*(14-len(f.stored_row(row))))
  edge=['opWire0001',2,2,'EDGE','','','about','opWire0001:1','opWire0001:1','self link for test','@me','S','t','']
  v=f.audit([stored,f.stored_row(edge)])['versions']['opWire0001:1']
  self.assertEqual((v['subject'],v['text'],v['by'],v['source'],v['at']),('007','=1+1 is not a formula','@me','(5) 3/4 TRUE','2026-11-14'))

class FastConfirm042(unittest.TestCase):
 """0.4.2: append receipt + whole-sheet op count replaces the positional read-back."""
 def setUp(self):
  self.rows=[f.wire_row(r) for r in [['opAbc12345xyz',1,2,'NODE','','','Knowledge','t','','x','me','S','s'],['opAbc12345xyz',2,2,'EDGE','','','about','opAbc12345xyz:1','p:1','y','me','S','s']]]
 def rec(self,rows=2,cells=26,status='success',rng='Memory!A3:M4'):return {'status':status,'updates':{'updatedRows':rows,'updatedCells':cells,'updatedRange':rng}}
 def test_verified(self):self.assertEqual(f.confirm(self.rows,self.rec(),2),'verified')
 def test_wrong_updated_range_ignored(self):self.assertEqual(f.confirm(self.rows,self.rec(rng='Memory!A99:M100'),2),'verified')
 def test_count_before_append_recounts_once(self):
  self.assertEqual(f.confirm(self.rows,self.rec(),0),'recount');self.assertEqual(f.confirm(self.rows,self.rec(),0,True),'pending')
 def test_duplicates_or_collision(self):self.assertEqual(f.confirm(self.rows,self.rec(),4),'check_duplicates')
 def test_partial(self):self.assertEqual(f.confirm(self.rows,self.rec(rows=1,cells=13),1),'pending')
 def test_failed_receipt_rows_present_need_check(self):self.assertEqual(f.confirm(self.rows,self.rec(status='error'),2),'check_duplicates')
 def test_no_count_uncertain(self):self.assertEqual(f.confirm(self.rows,self.rec(),None),'uncertain')
 def test_cell_mismatch_not_verified(self):self.assertNotEqual(f.confirm(self.rows,self.rec(cells=25),2),'verified')
 def test_count_request_shape(self):
  r=f.count_request('opAbc12345xyz',7)[0]['findReplace'];self.assertEqual((r['find'],r['replacement'],r['range'],r['matchEntireCell'],r['matchCase']),('opAbc12345xyz','opAbc12345xyz',{'sheetId':7,'startColumnIndex':0,'endColumnIndex':1},True,True))
  self.assertNotIn('sheetId',r)  # never whole-sheet scope: live overcount 3 vs 1
 def test_unsafe_tokens_refused(self):
  for bad in ('1e345678','TRUE12345','opshort','op-has-dash12','12345678','=op123456789'):
   self.assertFalse(f.new_op_ok(bad))
  with self.assertRaises(f.Invalid):f.count_request('1e345678')
 def test_new_tokens_still_valid_rows(self):self.assertEqual(len(f.audit([f.stored_row(r[:1]+[1,1]+r[3:]) for r in [['opAbc12345xyz',1,1,'NODE','','','Knowledge','t','','x','me','S','s']]])['heads']),1)

class FastConfirmLive042(unittest.TestCase):
 def test_live_reply_shapes(self):
  self.assertEqual(f.count_from_reply({'replies':[{'findReplace':{}}],'status':'success'}),0)
  self.assertEqual(f.count_from_reply({'replies':[{'findReplace':{'valuesChanged':4,'rowsChanged':4,'sheetsChanged':1,'occurrencesChanged':4}}]}),4)
  self.assertIsNone(f.count_from_reply({'replies':[{}]}))

class TailWindow043(unittest.TestCase):
 """0.4.3: default verification reads a window after the last seen row and matches op + exact content."""
 def setUp(self):
  self.n=['opWin123456ab',1,2,'NODE','','','Knowledge','t/x','','=1+1 and 007','me','S','s']
  self.e=['opWin123456ab',2,2,'EDGE','','','about','opWin123456ab:1','p:1','y','me','S','s']
  self.w=[f.wire_row(self.n),f.wire_row(self.e)];self.st=[f.stored_row(self.n),f.stored_row(self.e)]
  self.other=['opOther99999x','1','1','NODE','','','Knowledge','t/o','','o','them','S','s']
 def test_window_range(self):self.assertEqual(f.window_range(20008),'Memory!A20009:N20028')
 def test_verified_after_other_writers(self):self.assertEqual(f.locate([self.other,self.other]+self.st,self.w),('verified',3))
 def test_content_change_detected(self):
  bad=[list(self.st[0]),self.st[1]];bad[0][9]='edited';self.assertEqual(f.locate(bad,self.w)[0],'conflict')
 def test_partial(self):self.assertEqual(f.locate([self.st[0]],self.w)[0],'pending')
 def test_not_seen_short_window(self):self.assertEqual(f.locate([self.other],self.w)[0],'not_seen')
 def test_beyond_full_window(self):self.assertEqual(f.locate([self.other]*20,self.w)[0],'beyond')
 def test_receipt_position_never_used(self):self.assertNotIn('updatedRange',open(f.__file__).read().split('0.4.3 default verification')[1])
