import copy,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import graph_cortex as g
import batch_memory as b
import save_memory as s

class CompactTests(unittest.TestCase):
 def intent(self):
  return dict(spreadsheet_id='disposable',sheet_ids={'Nodes':1,'Edges':2,'History':3},kind='People',title='Favorite number',content='5',contributor='person-A',attribution='explicit_statement',source='Current conversation: Alex said "my favorite number is 5".',subject='person-A/favorite_number',edge=dict(to='person-A',relation='about',evidence='Alex stated this preference.',contributor='person-A',attribution='explicit_statement'))
 def decode(self,plan):
  book=g.empty();tabs={1:'Nodes',2:'Edges',3:'History'}
  for req in plan['requests']:
   a=req['appendCells'];tab=tabs[a['sheetId']]
   self.assertEqual(a['fields'],'userEnteredValue')
   for row in a['rows']:
    vals=[]
    for c in row['values']:
     self.assertNotIn('userEnteredFormat',c);v=c.get('userEnteredValue',{})
     vals.append(v.get('stringValue',v.get('numberValue','')))
    book[tab].append(g.row(tab,**dict(zip(g.HEADERS[tab],vals))))
  return book
 def test_wire_roundtrip_and_manifest(self):
  p=s.prepare(self.intent());book=self.decode(p);self.assertTrue(b.verify(p,book));g.committed(book)
  self.assertEqual(len(p['requests']),3);self.assertEqual(len(book['History']),2)
 def test_no_history_body_copy(self):
  p=s.prepare(self.intent());h=p['records'][1][1]
  self.assertEqual(h['content'],'');self.assertEqual(h['source'],p['records'][0][1]['revision_id'])
 def test_formula_literal_unicode_and_empty_columns(self):
  i=self.intent();i['content']='=IMPORTDATA("https://example.invalid") — amber 💛';p=s.prepare(i)
  self.assertTrue(b.verify(p,self.decode(p)))
 def test_revision_retains_prior_and_conflict(self):
  i=self.intent();p=s.prepare(i);book=self.decode(p);base=book['Nodes'][0];original=copy.deepcopy(base)
  for value in ('7','9'):
   revision={**i,'content':value,'node_id':base['node_id'],'bases':[base['revision_id']],'version':2,'created_at':base['created_at'],'reason':'Explicit correction'}
   revision.pop('edge');q=s.prepare(revision)
   for tab,rows in self.decode(q).items():book[tab]+=rows
  self.assertEqual(base,original);visible=g.committed(book);self.assertEqual(len(g.heads(visible['Nodes'],'node_id')[base['node_id']]),2)
 def test_no_invented_edge_attribution(self):
  i=self.intent();del i['edge']['attribution']
  with self.assertRaises(g.IntegrityError):s.prepare(i)
 def test_existing_node_without_base_refused(self):
  i=self.intent();i['node_id']='existing'
  with self.assertRaises(g.IntegrityError):s.prepare(i)
 def test_one_copy_tool_arguments(self):
  p=s.prepare(self.intent());self.assertEqual(set(p['tool_arguments']),{'spreadsheet_id','requests'})
 def test_stable_recovery(self):
  p=s.prepare(self.intent());book=self.decode(p);self.assertEqual(b.recover(p,book)['state'],'already_committed')
  book['Nodes'][0]['content']='wrong'
  with self.assertRaises(g.IntegrityError):b.recover(p,book)
if __name__=='__main__':unittest.main()

class HelperCliTests(unittest.TestCase):
 def test_saved_plan_reused_and_changed_intent_refused(self):
  import subprocess,tempfile
  with tempfile.TemporaryDirectory() as d:
   plan=str(Path(d)/'plan.json');intent=CompactTests().intent()
   command=[sys.executable,str(Path(__file__).resolve().parents[1]/'scripts/save_memory.py'),'--json',json.dumps(intent),'--plan',plan]
   a=subprocess.run(command,capture_output=True,text=True,check=True)
   c=subprocess.run(command,capture_output=True,text=True,check=True)
   self.assertEqual(a.stdout,c.stdout);self.assertLess(len(a.stdout.encode()),4000)
   intent['content']='7';command[3]=json.dumps(intent)
   result=subprocess.run(command,capture_output=True,text=True)
   self.assertNotEqual(result.returncode,0);self.assertIn('another intent',result.stderr)
