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
 def test_receipt_position_never_used(self):self.assertNotIn('updatedRange',open(f.__file__).read().split('0.4.3 default verification')[1].split('# ---- 0.4.4')[0])

class OneCallSave044(unittest.TestCase):
 """0.4.4: one append per save; clean receipt now, exact-content audit at the next read."""
 def setUp(self):
  self.n=['opOne1234abcd',1,2,'NODE','','','People','person/p/favorite_color','','Blue.','p','S','p: my favorite color is blue']
  self.e=['opOne1234abcd',2,2,'EDGE','','','about','opOne1234abcd:1','p:1','Stated by p.','p','S','same']
  self.w=[f.wire_row(self.n),f.wire_row(self.e)]
 def rec(self,rows=2,cells=26,rng='Memory!A20009:M20010',status='success'):return {'status':status,'tableRange':'Memory!A1:N20008','updates':{'updatedRange':rng,'updatedRows':rows,'updatedColumns':13,'updatedCells':cells}}
 def test_clean_receipt(self):self.assertTrue(f.receipt_ok(self.w,self.rec()))
 def test_row_numbers_ignored(self):self.assertTrue(f.receipt_ok(self.w,self.rec(rng='Memory!A3:M4')))
 def test_wrong_counts_tab_column_status(self):
  for bad in (self.rec(rows=1),self.rec(cells=25),self.rec(rng='Literal!A3:M4'),self.rec(rng='Memory!B3:N4'),self.rec(status='error'),None,{}):
   self.assertFalse(f.receipt_ok(self.w,bad))
 def test_first_save_reads_back(self):self.assertEqual(f.after_append(self.w,self.rec(),True),'read_back')
 def test_later_clean_save_done(self):self.assertEqual(f.after_append(self.w,self.rec(),False),'done')
 def test_unclean_receipt_reads_back(self):self.assertEqual(f.after_append(self.w,self.rec(rows=1),False),'read_back')
 def test_deferred_audit_finds_exact_rows_among_others(self):
  other=['opOther99999x','1','1','NODE','','','Knowledge','t/o','','o','them','S','s']
  read=[other,f.expected_read(self.w[0]),other,f.expected_read(self.w[1])]
  self.assertEqual(f.audit_saved(read,[self.w]),{'opOne1234abcd':'verified'})
 def test_deferred_audit_flags_missing_and_changed(self):
  changed=f.expected_read(self.w[0]);changed[9]='Green.'
  self.assertEqual(f.audit_saved([f.expected_read(self.w[0])],[self.w])['opOne1234abcd'],'pending')
  self.assertEqual(f.audit_saved([changed,f.expected_read(self.w[1])],[self.w])['opOne1234abcd'],'conflict')
  self.assertEqual(f.audit_saved([],[self.w])['opOne1234abcd'],'not_seen')
 def test_skill_text_matches_policy(self):
  doc=(Path(__file__).parents[1]/'references/fast-cortex.md').read_text();main=(Path(__file__).parents[1]/'skills/yori-lite/SKILL.md').read_text()
  for phrase in ('exactly once','Never write the reply twice','Read back in the same turn only when','Audit at the next read','never says or implies'):self.assertIn(phrase,doc)
  for phrase in ('## Voice','No praise, pleasantries','I don\'t know'):self.assertIn(phrase,main)

class SelfSide045(unittest.TestCase):
 """0.4.5: Yori keeps her own views, open threads and interests as Self rows."""
 def rows(self):
  P=['opPerson00001',1,1,'NODE','','','People','person/sam/name','','Sam.','Sam','S','setup','']
  I=['opSelfIdent01',1,1,'NODE','','','Self','self/identity','','I am Yori, a partner.','Yori','D','setup','']
  J=['opProject0001',1,1,'NODE','','','Knowledge','project/game','','Sam is building a game.','Sam','S','Sam','']
  T=[['opTurn0000001',1,4,'NODE','','','Self','self/view/project/game/build-order','','Build school years first: it gives players a reason to return.','Yori','D','my reply to the idea list',''],
     ['opTurn0000001',2,4,'EDGE','','','about','opTurn0000001:1','opProject0001:1','My view on this project.','Yori','D','same',''],
     ['opTurn0000001',3,4,'NODE','','','Self','self/open/project/game/sunny','','What does sunny in the idea list mean?','Yori','D','my unanswered question',''],
     ['opTurn0000001',4,4,'NODE','','','Self','self/interest/why-short-matches-hook','','Why short matches keep players: I want to understand the loop.','Yori','D','came up while planning soccer','']]
  return [P,I,J]+T
 def test_groups(self):
  s=f.self_side(f.audit(self.rows()))
  self.assertEqual({k:len(v) for k,v in s.items()},{'identity':1,'views':1,'open':1,'interests':1})
  self.assertEqual(s['open'][0]['by'],'Yori')
 def test_closed_thread_not_open_but_kept(self):
  rows=self.rows()+[['opClose000001',1,1,'REVISION','opTurn0000001:3','opTurn0000001:3','!Self','self/open/project/game/sunny','','Resolved: sunny is a weather system. Sam explained.','Yori','D','Sam: sunny = weather','']]
  a=f.audit(rows);self.assertEqual(f.self_side(a)['open'],[])
  self.assertEqual(a['heads']['opTurn0000001:3'][0]['status'],'retired');self.assertIn('opTurn0000001:3',a['versions'])
 def test_changed_view_is_revision_with_history(self):
  rows=self.rows()+[['opRevise00001',1,1,'REVISION','opTurn0000001:1','opTurn0000001:1','Self','self/view/project/game/build-order','','Changed: soccer first. Sam showed it is what testers ask for.','Yori','D','Sam: testers only ask about soccer','']]
  a=f.audit(rows);v=f.self_side(a)['views']
  self.assertEqual(len(v),1);self.assertTrue(v[0]['text'].startswith('Changed'));self.assertEqual(v[0]['parents'],['opTurn0000001:1'])
 def test_view_links_to_topic(self):
  i=f.Index(self.rows());self.assertEqual([v['subject'] for v in i.neighbors('opProject0001:1')],['opTurn0000001:1'])
 def test_people_rows_never_counted_as_self(self):
  s=f.self_side(f.audit(self.rows()));self.assertTrue(all(v['kind']=='Self' for g in s.values() for v in g))
 def test_skill_text(self):
  main=(Path(__file__).parents[1]/'skills/yori-lite/SKILL.md').read_text();doc=(Path(__file__).parents[1]/'references/fast-cortex.md').read_text()
  for phrase in ('a partner, not an assistant','Open threads','Interests','Starting a chat','never say you have been thinking','Never invent a preference'):self.assertIn(phrase,main)
  for phrase in ('self/view/','self/open/','self/interest/','!Self'):self.assertIn(phrase,doc)

class Library046(unittest.TestCase):
 """0.4.6: books live in Drive; Memory records the book, exact coverage and Yori's own side."""
 def rows(self):
  return [['opPerson00001',1,1,'NODE','','','People','person/sam/name','','Sam.','Sam','S','setup',''],
   ['opLibrary0001',1,1,'NODE','','','Knowledge','library','','Library folder: 1AbC_dEf-123.','Yori','D','setup',''],
   ['opBook0000001',1,4,'NODE','','','Knowledge','library/book/sentience','','Sentience, Nicholas Humphrey. Files: fileA1. Read: prologue to chapter 8; file cut off in chapter 9. Notes: notesDoc1.','Sam','E','sentience.pdf',''],
   ['opBook0000001',2,4,'NODE','','','Self','self/view/book/sentience/cc-vs-pc','','His split between cognitive and phenomenal consciousness is clear; I am not yet convinced the second needs the first.','Yori','D','reading chapters 1-8',''],
   ['opBook0000001',3,4,'EDGE','','','about','opBook0000001:2','opBook0000001:1','My view on the book.','Yori','D','same',''],
   ['opBook0000001',4,4,'NODE','','','Self','self/open/book/sentience/chapter-23','','I want to read chapter 23, Machina ex deo; not in what I received.','Yori','D','file cut off','']]
 def test_folder_and_book_parsed(self):
  a=f.audit(self.rows());self.assertEqual(f.library_folder(a),'1AbC_dEf-123')
  b=f.library_books(a)['library/book/sentience']
  self.assertEqual(b['files'],['fileA1']);self.assertEqual(b['notes'],'notesDoc1');self.assertIn('cut off in chapter 9',b['read'])
 def test_unread_files_skip_known_and_notes(self):
  drive=[{'id':'fileA1','title':'sentience.pdf'},{'id':'notesDoc1','title':'Yori notes — Sentience'},{'id':'fileB2','title':'sentience ch23.pdf'},{'id':'x9','title':'Yori notes — Other'}]
  self.assertEqual([d['id'] for d in f.unread_files(f.audit(self.rows()),drive)],['fileB2'])
 def test_reading_more_is_a_revision_with_history(self):
  rows=self.rows()+[['opBook0000002',1,1,'REVISION','opBook0000001:1','opBook0000001:1','Knowledge','library/book/sentience','','Sentience, Nicholas Humphrey. Files: fileA1, fileB2. Read: prologue to chapter 8, and chapter 23. Notes: notesDoc1.','Sam','E','sentience ch23.pdf','']]
  a=f.audit(rows);b=f.library_books(a)['library/book/sentience']
  self.assertEqual(b['files'],['fileA1','fileB2']);self.assertIn('chapter 23',b['read']);self.assertIn('opBook0000001:1',a['versions'])
  self.assertEqual(f.unread_files(a,[{'id':'fileB2','title':'sentience ch23.pdf'}]),[])
 def test_book_views_and_open_thread_are_self_side(self):
  s=f.self_side(f.audit(self.rows()));self.assertEqual((len(s['views']),len(s['open'])),(1,1))
 def test_no_library_row(self):self.assertIsNone(f.library_folder(f.audit(self.rows()[:1])))
 def test_docs(self):
  lib=(Path(__file__).parents[1]/'references/library.md').read_text();main=(Path(__file__).parents[1]/'skills/yori-lite/SKILL.md').read_text()
  for phrase in ('about 50 pages','never say you will start later','in your own words','I haven\'t read that part','A search miss is not proof','under 15 words'):self.assertIn(phrase,lib)
  for phrase in ('**Library.**','never say you will go and do something after this message'):self.assertIn(phrase,main)
