"""Static instruction checks and local models; not a live Claude/Drive test."""
import copy
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]

class GuideStore:
    def __init__(self,files=None):self.files=copy.deepcopy(files or {});self.created=[];self.fail_readback=False
    def create(self,parent,body):
        key='guide-'+str(len(self.files)+1)
        self.files[key]={'parent':parent,'body':body,'role':'config_guide','description':'record_type: human_readme'}
        self.created.append(key);return key
    def read(self,key):
        if self.fail_readback:raise RuntimeError('read-back failed')
        return copy.deepcopy(self.files[key])

def ensure_guide_model(store,parent,body):
    # Conservative creation-only model of README_MIGRATION.md; no updates/deletions.
    candidates=[(k,f) for k,f in store.files.items() if f.get('parent')==parent and f.get('role')=='config_guide']
    if len(candidates)>1:raise ValueError('ambiguous')
    if candidates:
        key,f=candidates[0]
        if store.read(key).get('body'):return key
        raise ValueError('incomplete new guide')
    readable=[(k,f) for k,f in store.files.items() if f.get('parent')==parent and f.get('name','').startswith('README') and f.get('body')]
    if len(readable)>1:raise ValueError('ambiguous')
    if readable:return readable[0][0]
    key=store.create(parent,body)
    observed=store.read(key)
    if observed['body']!=body or observed['parent']!=parent:raise RuntimeError('verification')
    return key

class ReadmeMigrationTests(unittest.TestCase):
    def setUp(self):
        self.originals={
            'config':{'parent':'config_plugins','description':'existing pointer','body':''},
            'self':{'parent':'Self','description':'developing identity','body':''},
            'memory':{'parent':'Knowledge','description':'Aurora facts','body':''},
            'history':{'parent':'History','description':'original contribution','body':''},
            'readme':{'parent':'config_plugins','name':'README','description':'old metadata instructions','body':''}}
        self.body=(ROOT/'templates/config_plugins_README.md').read_text()
    def test_metadata_readme_gets_additive_readable_body(self):
        store=GuideStore(self.originals);key=ensure_guide_model(store,'config_plugins',self.body)
        self.assertEqual(store.files[key]['body'],self.body)
        for k,v in self.originals.items():self.assertEqual(store.files[k],v)
    def test_second_run_does_not_duplicate(self):
        store=GuideStore(self.originals);a=ensure_guide_model(store,'config_plugins',self.body);b=ensure_guide_model(store,'config_plugins',self.body)
        self.assertEqual(a,b);self.assertEqual(len(store.created),1)
    def test_existing_custom_readable_readme_untouched(self):
        store=GuideStore(self.originals);store.files['readme']['body']='Our custom guide'
        before=copy.deepcopy(store.files);self.assertEqual(ensure_guide_model(store,'config_plugins',self.body),'readme')
        self.assertEqual(store.files,before);self.assertEqual(store.created,[])
    def test_failed_readback_does_not_claim_success_or_reset_cortex(self):
        store=GuideStore(self.originals);store.fail_readback=True
        with self.assertRaises(RuntimeError):ensure_guide_model(store,'config_plugins',self.body)
        for k,v in self.originals.items():self.assertEqual(store.files[k],v)
        store.fail_readback=False;ensure_guide_model(store,'config_plugins',self.body)
        self.assertEqual(len(store.created),1)
    def test_duplicate_guides_stop_without_mutation(self):
        store=GuideStore(self.originals);store.create('config_plugins',self.body);store.create('config_plugins',self.body)
        before=copy.deepcopy(store.files)
        with self.assertRaises(ValueError):ensure_guide_model(store,'config_plugins',self.body)
        self.assertEqual(store.files,before)
    def test_other_folder_guide_is_not_reused(self):
        store=GuideStore(self.originals);other=store.create('OtherCortex','unrelated')
        guide=ensure_guide_model(store,'config_plugins',self.body)
        self.assertNotEqual(guide,other);self.assertEqual(store.files[other]['body'],'unrelated')

class InstructionRegressionTests(unittest.TestCase):
    def test_all_skills_have_colleague_habits_and_turn_reuse(self):
        for p in (ROOT/'skills').glob('*/SKILL.md'):
            s=p.read_text()
            for phrase in ['generic engagement questions','Do not offer three choices','reasoned opinions','A complete thought can simply end','Do not announce every memory','Share one verified turn context']:
                self.assertIn(phrase,s,p)
            self.assertNotIn('What would you like me to know?',s)
    def test_setup_finishes_and_guide_uses_body(self):
        s=(ROOT/'skills/yori-lite-connect/SKILL.md').read_text()
        self.assertIn('Then stop.',s);self.assertIn('readable Google Doc body',s)
        self.assertNotIn('leave contents empty. Preserve other plugins',s)
    def test_example_cases_are_editorial_fixtures_not_model_outputs(self):
        cases=json.loads((ROOT/'tests/conversation_cases.json').read_text())
        self.assertEqual(len(cases),8)
        for c in cases:
            self.assertTrue(c['check'])
            if not c['question_needed']:self.assertNotIn('?',c['example'])
        self.assertIn("don't think",next(c for c in cases if c['case']=='disagreement')['example'])
    def test_schema_and_identity_stay_v1_single_cortex(self):
        schema=json.loads((ROOT/'schemas/config.schema.json').read_text())
        self.assertEqual(schema['properties']['schema_version']['const'],1)
        self.assertEqual(schema['properties']['plugin_id']['const'],'yori_2d970fa0-89e4-451e-802b-9f836f99d9e1')
        self.assertEqual(schema['required'],['schema_version','plugin_id','active_cortex'])

class SchedulingModelTests(unittest.TestCase):
    def test_eight_calls_can_form_six_dependency_stages(self):
        deps={'create_contribution':set(),'read_base':set(),
              'verify_contribution':{'create_contribution'},'create_snapshot':{'read_base','verify_contribution'},
              'verify_snapshot':{'create_snapshot'},'parent_check':{'read_base','create_snapshot'},
              'patch':{'verify_contribution','verify_snapshot','parent_check'},'verify_patch':{'patch'}}
        done=set();stages=[]
        while len(done)<len(deps):
            stage={k for k,v in deps.items() if k not in done and v<=done}
            self.assertTrue(stage);stages.append(stage);done|=stage
        self.assertEqual(len(done),8);self.assertEqual(len(stages),6)
        self.assertLess(next(i for i,s in enumerate(stages) if 'verify_snapshot' in s),next(i for i,s in enumerate(stages) if 'patch' in s))
        self.assertEqual(stages[-1],{'verify_patch'})
    def test_safety_checks_not_replaced_by_latency_target(self):
        s=(ROOT/'TURN_EFFICIENCY.md').read_text()
        self.assertIn('Never omit a guard or a required read-back',s)
        self.assertIn('NOT measured Google latency',s)
        self.assertIn('No blanket full-Cortex scan',s)

if __name__=='__main__':unittest.main()
