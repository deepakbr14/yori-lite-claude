"""Local eligibility/instruction tests; not a runtime or Google test."""
import copy,hashlib,json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
LEGACY=(ROOT/'references/legacy/cortex-readme-0.2.1.txt').read_bytes()

class GuardConflict(Exception):pass

def eligible(file,root_id,receipt=False):
    if file.get('parent')!=root_id or file.get('name')!='README - About this Cortex.txt' or file.get('trashed'):return False
    marker=file.get('metadata',{})
    allowed={'record_type','role','guide_version','operation_id'}
    if set(marker)-allowed:return False
    generated=(marker.get('record_type')=='human_readme' and marker.get('role')=='cortex_guide' and marker.get('guide_version')=='0.2.1')
    return (receipt or generated) and file.get('body')==LEGACY and bool(file.get('etag'))

def trash_model(store,key,observed,root_id,guard=True,receipt=False):
    # Reversible metadata change only, after identity/body/scope checks.
    if not guard or not eligible(observed,root_id,receipt):return False
    current=store[key]
    if current['parent']!=observed['parent']:return False
    if current['etag']!=observed['etag']:raise GuardConflict()
    current['trashed']=True;current['etag']+=1
    return current['trashed']

class SafeGuideRetirementTests(unittest.TestCase):
    def setUp(self):
        self.f={'name':'README - About this Cortex.txt','parent':'chosen','body':LEGACY,'etag':3,'trashed':False,'metadata':{'record_type':'human_readme','role':'cortex_guide','guide_version':'0.2.1','operation_id':'old-op'}}
    def test_exact_known_generated_guide_is_recoverably_trashed(self):
        store={'readme':copy.deepcopy(self.f),'memory':{'description':'do not touch'},'config':{'description':'same pointer'}}
        memory=copy.deepcopy(store['memory']);config=copy.deepcopy(store['config'])
        self.assertTrue(trash_model(store,'readme',copy.deepcopy(self.f),'chosen'))
        self.assertEqual(store['memory'],memory);self.assertEqual(store['config'],config)
        self.assertEqual(store['readme']['body'],LEGACY)
    def test_user_edit_is_preserved(self):
        self.f['body']+=b'\nOur crew rules.';self.assertFalse(eligible(self.f,'chosen'))
    def test_unmarked_same_name_is_not_provenance(self):
        self.f['metadata']={};self.assertFalse(eligible(self.f,'chosen'))
    def test_known_receipt_allows_exact_unmarked_generated_file(self):
        self.f['metadata']={};self.assertTrue(eligible(self.f,'chosen',receipt=True))
    def test_memory_in_metadata_is_preserved(self):
        self.f['metadata']['note']='Mara is navigator';self.assertFalse(eligible(self.f,'chosen'))
    def test_wrong_parent_or_name_is_preserved(self):
        self.assertFalse(eligible(self.f,'other'))
        self.f['name']='README';self.assertFalse(eligible(self.f,'chosen'))
    def test_guard_unavailable_means_no_trash(self):
        store={'r':copy.deepcopy(self.f)};self.assertFalse(trash_model(store,'r',self.f,'chosen',guard=False));self.assertEqual(store['r'],self.f)
    def test_changed_etag_rejects_trash(self):
        observed=copy.deepcopy(self.f);store={'r':copy.deepcopy(self.f)};store['r']['etag']+=1;store['r']['body']+=b'user addition'
        with self.assertRaises(GuardConflict):trash_model(store,'r',observed,'chosen')
        self.assertFalse(store['r']['trashed'])
    def test_move_with_same_etag_blocks_cleanup(self):
        store={'r':copy.deepcopy(self.f)};store['r']['parent']='other'
        self.assertFalse(trash_model(store,'r',self.f,'chosen'));self.assertFalse(store['r']['trashed'])
    def test_legacy_fixture_hash_is_exact(self):
        catalog=json.loads((ROOT/'references/legacy/guide-identities.json').read_text())
        self.assertEqual(hashlib.sha256(LEGACY).hexdigest(),catalog['cortex_guide_0_2_1']['sha256'])

class EntryAndInstructionTests(unittest.TestCase):
    def test_short_main_and_hidden_helpers_without_duplicate_commands(self):
        main=(ROOT/'skills/yori-lite/SKILL.md').read_text()
        self.assertIn('name: yori-lite\n',main);self.assertIn('## Main entry point',main)
        self.assertNotIn('user-invocable: false',main)
        self.assertFalse((ROOT/'commands').exists())
        for p in (ROOT/'skills').glob('*/SKILL.md'):
            if p.parent.name!='yori-lite':self.assertIn('user-invocable: false',p.read_text())
    def test_contract_is_shared_and_account_not_inferred(self):
        contract=(ROOT/'references/operating-contract.md').read_text()
        self.assertIn('Missing configuration is an ordinary setup state',contract)
        self.assertIn('Account email identification is optional, never a prerequisite',contract)
        self.assertIn('never infer it from an existing file owner',contract)
        for p in (ROOT/'skills').glob('*/SKILL.md'):
            self.assertIn('../../references/operating-contract.md',p.read_text())
    def test_one_step_setup_and_no_new_cortex_guide(self):
        connect=(ROOT/'skills/yori-lite-connect/SKILL.md').read_text()
        self.assertIn('The Cortex has NO setup README',connect)
        self.assertIn('Show no URL',connect)
        self.assertIn('And stop.',connect)
        self.assertFalse((ROOT/'templates/cortex_README.txt').exists())
    def test_registry_guide_is_vendor_neutral_with_two_plugins(self):
        text=(ROOT/'templates/config_plugins_README.md').read_text()
        self.assertIn('Atlas',text);self.assertIn('Planner',text)
        self.assertIn('not an official Google, Claude, or ChatGPT standard',text)
        self.assertIn('duplicate names',text)
        self.assertNotIn('Yori Lite uses',text)
    def test_purposeful_question_filter_keeps_real_curiosity(self):
        text=(ROOT/'references/operating-contract.md').read_text()
        self.assertIn('Do not forbid all questions',text)
        self.assertIn("I'd give Aurora a recognizable silhouette",text)
    def test_new_topic_learning_and_verification_not_removed(self):
        text=(ROOT/'TURN_EFFICIENCY.md').read_text()
        self.assertIn('Keep both.',text)
        self.assertIn('contribution create/read-back followed by topic create/read-back',text)
        self.assertIn('do not establish a 3-second improvement',text)
    def test_static_text_measurement_honest_and_smaller(self):
        m=json.loads((ROOT/'tests/INSTRUCTION_SIZE.json').read_text())
        self.assertEqual(m['new_five_skill_bytes'],sum(len(p.read_bytes()) for p in (ROOT/'skills').glob('*/SKILL.md')))
        self.assertEqual(m['new_shared_contract_bytes'],len((ROOT/'references/operating-contract.md').read_bytes()))
        self.assertLess(m['new_five_skill_bytes']+m['new_shared_contract_bytes'],m['previous_five_skill_bytes'])

if __name__=='__main__':unittest.main()
