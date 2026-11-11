"""Disposable in-memory fault model, NOT an executable plugin or Claude/Drive test.
Structured test claims make provenance auditable; production descriptions remain prose.
"""
import copy
import unittest
import uuid

class IntegrityError(Exception): pass

class Store:
    def __init__(self):
        self.files={}; self.readback_failure=False; self.snapshot_failure=False
    def create(self,kind,payload,parent):
        key=str(uuid.uuid4())  # local provider stand-in, never a production ID generator
        self.files[key]={'id':key,'kind':kind,'payload':copy.deepcopy(payload),
                         'parent':parent,'etag':1,'name':kind}
        return key
    def read(self,key):
        if self.readback_failure: raise IntegrityError('read-back failed')
        return copy.deepcopy(self.files[key])
    def initialize(self,key,payload,receipt,etag):
        f=self.files[key]
        if receipt!=key or f['payload'] or f['etag']!=etag:raise IntegrityError('not owned empty initialization')
        f['payload']=copy.deepcopy(payload);f['etag']+=1
        return self.read(key)
    def patch(self,key,payload,etag):
        f=self.files[key]
        if f['parent']=='History':raise IntegrityError('committed History cannot be patched')
        if f['etag']!=etag:raise IntegrityError('conflict')
        f['payload']=copy.deepcopy(payload);f['etag']+=1
    def validate_ref(self,key,kind,parent):
        f=self.read(key)
        if f['kind']!=kind or f['parent']!=parent:raise IntegrityError('wrong reference')
        return f
    def contribution(self,claims):
        for c in claims:
            if c['category']=='explicit' and (c['basis']!='utterance' or c['author']=='Yori'):
                raise IntegrityError('inference laundered as person statement')
            if c['category'] in ('inference','decision') and c['author']!='Yori':raise IntegrityError('wrong author')
            if c.get('attribute') and not c.get('attribute_evidence'):raise IntegrityError('unsupported attribute')
        key=self.create('contribution',{'claims':claims},'History')
        self.validate_ref(key,'contribution','History')
        return key
    def update(self,target,base,contribution,current,*,before_patch=None):
        self.validate_ref(contribution,'contribution','History')
        snap=self.create('prior_revision',{'source':target,'etag':base['etag'],
            'description':base['payload'],'name':base['name'],'operation_id':contribution},'History')
        if self.snapshot_failure:raise IntegrityError('snapshot read-back failed')
        self.validate_ref(snap,'prior_revision','History')
        if before_patch:before_patch()
        if self.read(target)['parent']!=base['parent']:raise IntegrityError('moved')
        payload=copy.deepcopy(current);payload.update(operation_id=contribution,prior=snap)
        self.patch(target,payload,base['etag'])
        if self.read(target)['payload']!=payload:raise IntegrityError('unverified')
        return snap

def claim(category,author,text,basis,**kw):
    return dict(category=category,author=author,text=text,basis=basis,**kw)

class IntegrityTests(unittest.TestCase):
    def setUp(self): self.s=Store()
    def test_color_experiment_and_fresh_reader(self):
        s=self.s
        first=s.contribution([claim('decision','Yori','amber: warmth without glare','own considered choice')])
        target=s.create('memory',{'color':'amber','reason':'warmth without glare','operation_id':first},'Self')
        s.read(target); committed={k:copy.deepcopy(v) for k,v in s.files.items() if v['parent']=='History'}
        suggestion=s.contribution([claim('explicit','person','Try red.','utterance'),claim('inference','Yori','May be a test; uncertain.','interpretation')])
        base=s.read(target);s.update(target,base,suggestion,dict(base['payload'],context='red suggested; preference unchanged'))
        insist=s.contribution([claim('explicit','person','No, make it red.','utterance'),claim('decision','Yori','Temporarily adopt red in response.','own decision')])
        base=s.read(target);s.update(target,base,insist,{'color':'red','reason':'temporary accommodation','original_reason':'warmth without glare'})
        explanation=s.contribution([claim('explicit','person','Your preferences should remain your own.','utterance')])
        base=s.read(target);s.update(target,base,explanation,dict(base['payload'],context='person clarified autonomy'))
        revisit=s.contribution([claim('decision','Yori','Return to amber for warmth without glare.','own considered choice')])
        base=s.read(target);s.update(target,base,revisit,{'color':'amber','reason':'warmth without glare','context':'red was temporary accommodation'})
        fresh=Store();fresh.files=copy.deepcopy(s.files)  # fresh reader, no chat state
        current=fresh.read(target)['payload'];self.assertEqual(current['color'],'amber')
        for k,v in committed.items():self.assertEqual(s.files[k],v)
        snapshots=[f['payload'] for f in s.files.values() if f['kind']=='prior_revision']
        self.assertEqual(len(snapshots),4)
        self.assertEqual([x['description']['color'] for x in snapshots],['amber','amber','red','red'])
        for f in s.files.values():
            p=f['payload']
            if 'operation_id' in p:fresh.validate_ref(p['operation_id'],'contribution','History')
            if 'prior' in p:fresh.validate_ref(p['prior'],'prior_revision','History')
        inferred=[c for f in s.files.values() if f['kind']=='contribution' for c in f['payload']['claims'] if 'test' in c['text']]
        self.assertEqual(inferred[0]['category'],'inference');self.assertEqual(inferred[0]['author'],'Yori')
    def test_person_inference_cannot_be_explicit(self):
        with self.assertRaises(IntegrityError):self.s.contribution([claim('explicit','person','It was a test.','interpretation')])
    def test_unknown_attributes_rejected_on_learning_and_revision(self):
        for attribute in ['pronouns','relationship','preference']:
            with self.assertRaises(IntegrityError):self.s.contribution([claim('inference','Yori','unsupported','guess',attribute=attribute)])
    def test_committed_history_technical_edit_rejected(self):
        k=self.s.contribution([claim('decision','Yori','amber','choice')]);before=self.s.read(k)
        with self.assertRaises(IntegrityError):self.s.patch(k,{'fixed_reference':'invented'},1)
        self.assertEqual(self.s.read(k),before)
    def test_correction_appended_not_rewritten(self):
        old=self.s.contribution([claim('inference','Yori','possibly a test','interpretation')]);before=self.s.read(old)
        correction=self.s.contribution([claim('decision','Yori','Retract the test inference.','correction',original_id=old)])
        self.assertNotEqual(old,correction);self.assertEqual(self.s.read(old),before)
    def test_blank_initialization_once(self):
        k=self.s.create('contribution',{},'History');self.s.initialize(k,{'claims':['technical probe only']},k,1)
        with self.assertRaises(IntegrityError):self.s.initialize(k,{'claims':['repair']},k,2)
    def test_lost_initialization_readback_does_not_allow_rewrite(self):
        k=self.s.create('contribution',{},'History');self.s.readback_failure=True
        with self.assertRaises(IntegrityError):self.s.initialize(k,{'claims':['committed']},k,1)
        self.s.readback_failure=False
        with self.assertRaises(IntegrityError):self.s.initialize(k,{'claims':['repaired']},k,2)
    def prepare(self):
        t=self.s.create('memory',{'color':'amber','reason':'warmth'},'Self')
        c=self.s.contribution([claim('decision','Yori','red','choice')]);return t,c
    def test_minor_edit_still_snapshots_exact_prior(self):
        t,c=self.prepare();base=self.s.read(t)
        snap=self.s.update(t,base,c,dict(base['payload'],technical_label='corrected'))
        self.assertEqual(self.s.read(snap)['payload']['description'],base['payload'])
    def test_snapshot_failure_blocks_current_patch(self):
        t,c=self.prepare();base=self.s.read(t);self.s.snapshot_failure=True
        with self.assertRaises(IntegrityError):self.s.update(t,base,c,{'color':'red'})
        self.assertEqual(self.s.read(t),base)
    def test_conflict_requires_snapshot_of_winning_version(self):
        t,c=self.prepare();base=self.s.read(t)
        with self.assertRaises(IntegrityError):self.s.update(t,base,c,{'color':'red'},before_patch=lambda:self.s.patch(t,{'color':'green','reason':'concurrent choice'},1))
        winner=self.s.read(t);snap=self.s.update(t,winner,c,{'color':'red','competing':'green retained'})
        self.assertEqual(self.s.read(snap)['payload']['description'],winner['payload'])
    def test_invalid_reference_blocks_patch(self):
        t,c=self.prepare();base=self.s.read(t)
        for bad in [t,'invented-reference']:
            with self.assertRaises((IntegrityError,KeyError)):self.s.update(t,base,bad,{'color':'red'})
        self.assertEqual(self.s.read(t),base)
    def test_out_of_scope_reference_blocks_patch(self):
        t,c=self.prepare();base=self.s.read(t);self.s.files[c]['parent']='OtherCortex'
        with self.assertRaises(IntegrityError):self.s.update(t,base,c,{'color':'red'})
        self.assertEqual(self.s.read(t),base)

if __name__=='__main__':unittest.main()
