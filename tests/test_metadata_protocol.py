"""Local model of the intended protocol, NOT Google/Claude execution or enforcement."""
import copy
import unittest

class Conflict(Exception): pass
class Moved(Exception): pass
class Unverified(Exception): pass

class DriveModel:
    def __init__(self):
        self.files={};self.next_id=0;self.guard=True;self.fail_history=False
    def create(self,name,description,parent):
        self.next_id+=1;key=f'f{self.next_id}'
        self.files[key]={'id':key,'name':name,'description':copy.deepcopy(description),'parent':parent,'etag':1}
        return key
    def read(self,key):return copy.deepcopy(self.files[key])
    def move(self,key,parent):self.files[key]['parent']=parent  # reported observed behavior
    def patch(self,key,description,expected_etag):
        if not self.guard:raise Unverified('guard unavailable')
        if self.files[key]['etag']!=expected_etag:raise Conflict()
        self.files[key]['description']=copy.deepcopy(description);self.files[key]['etag']+=1
    def history(self,operation_id,claim):
        # Scoped enumeration by operation_id, not filename. Preserve same receipt on retry.
        for key,f in self.files.items():
            if f['parent']=='History' and f['description'].get('record_type')=='contribution' and f['description'].get('operation_id')==operation_id:
                return key
        key=self.create('Contribution',{'record_type':'contribution','operation_id':operation_id,'claim':claim},'History')
        if self.fail_history:raise Unverified('read-back unavailable')
        assert self.read(key)['description']['claim']==claim
        return key
    def snapshot(self,base,op):
        return self.create('Prior revision',{'record_type':'prior_revision','operation_id':op,'source_id':base['id'],'source_etag':base['etag'],'prior':base['description']},'History')

def integrate(store,target,base,op,claim):
    receipt=store.history(op,claim)
    if not store.guard: return 'pending',receipt
    store.snapshot(base,op)
    if store.read(target)['parent']!=base['parent']:raise Moved()
    updated=copy.deepcopy(base['description'])
    updated['positions'][op]=claim
    updated['operation_id']=op
    store.patch(target,updated,base['etag'])
    readback=store.read(target)
    if readback['parent']!=base['parent']:raise Moved()
    if readback['description']!=updated:raise Unverified()
    return 'saved',receipt

class MetadataProtocolModelTests(unittest.TestCase):
    def setUp(self):
        self.d=DriveModel();self.t=self.d.create('Market X',{'positions':{'original':'A favors X: demand'},'status':'current'},'Knowledge')
    def test_two_writers_conflict_then_reconcile(self):
        base=self.d.read(self.t)
        integrate(self.d,self.t,base,'a','A: demand increased')
        with self.assertRaises(Conflict):integrate(self.d,self.t,base,'b','B: clearing costs too high')
        integrate(self.d,self.t,self.d.read(self.t),'b','B: clearing costs too high')
        self.assertEqual(set(self.d.read(self.t)['description']['positions']),{'original','a','b'})
        evidence=[f for f in self.d.files.values() if f['description'].get('record_type')=='contribution']
        self.assertEqual(len(evidence),2)
    def test_failed_reconciliation_keeps_both_contributions(self):
        base=self.d.read(self.t);integrate(self.d,self.t,base,'a','A view')
        with self.assertRaises(Conflict):integrate(self.d,self.t,base,'b','B dissent')
        self.assertTrue(any(f['description'].get('claim')=='B dissent' for f in self.d.files.values()))
        self.assertIn('a',self.d.read(self.t)['description']['positions'])
    def test_correction_preserves_previous_description(self):
        old=self.d.read(self.t)['description'];integrate(self.d,self.t,self.d.read(self.t),'correction','A retracts preference: new costs')
        snapshots=[f['description'] for f in self.d.files.values() if f['description'].get('record_type')=='prior_revision']
        self.assertTrue(any(s['prior']==old for s in snapshots))
        self.assertIn('original',self.d.read(self.t)['description']['positions'])
    def test_move_does_not_change_etag_but_blocks_update(self):
        base=self.d.read(self.t);self.d.move(self.t,'OtherCortex')
        self.assertEqual(base['etag'],self.d.read(self.t)['etag'])
        with self.assertRaises(Moved):integrate(self.d,self.t,base,'b','B view')
        self.assertEqual(self.d.read(self.t)['description'],base['description'])
    def test_missing_guard_saves_only_immutable_contribution(self):
        self.d.guard=False;base=self.d.read(self.t)
        status,_=integrate(self.d,self.t,base,'b','B view')
        self.assertEqual(status,'pending');self.assertEqual(self.d.read(self.t),base)
    def test_history_verification_failure_stops_shared_update(self):
        self.d.fail_history=True;base=self.d.read(self.t)
        with self.assertRaises(Unverified):integrate(self.d,self.t,base,'b','B view')
        self.assertEqual(self.d.read(self.t),base)
    def test_retry_same_operation_does_not_duplicate_contribution(self):
        receipt=self.d.history('op','same claim')
        self.assertEqual(receipt,self.d.history('op','same claim'))
    def test_ambiguous_update_can_be_detected_by_operation_id(self):
        base=self.d.read(self.t);integrate(self.d,self.t,base,'op','new claim')
        # A caller loses the response: read-back identifies the committed operation.
        self.assertEqual(self.d.read(self.t)['description']['operation_id'],'op')
        self.assertEqual(len([f for f in self.d.files.values() if f['description'].get('record_type')=='contribution']),1)
    def test_duplicate_names_preserve_distinct_ids(self):
        other=self.d.create('Market X',{'positions':{'b':'opposing view'}},'Knowledge')
        self.assertNotEqual(other,self.t);self.assertEqual(len(self.d.files),2)
    def test_stale_retirement_cannot_hide_new_contribution(self):
        base=self.d.read(self.t)
        replacement=self.d.create('Market X summary',base['description'],'Knowledge')
        integrate(self.d,self.t,base,'b','new dissent after summary')
        with self.assertRaises(Conflict):self.d.patch(self.t,{'status':'obsolete','replacement_id':replacement},base['etag'])
        self.assertEqual(self.d.read(self.t)['description']['status'],'current')
        self.assertIn('b',self.d.read(self.t)['description']['positions'])
    def test_model_exposes_external_move_race_not_a_transaction(self):
        base=self.d.read(self.t)
        # A move after a parent check still allows CAS: it is not parent isolation.
        self.d.move(self.t,'OtherCortex')
        self.d.patch(self.t,{'positions':{'x':'update'}},base['etag'])
        self.assertEqual(self.d.read(self.t)['parent'],'OtherCortex')
        # This known residual risk is documented; avoiding active moves is the default.

if __name__=='__main__':unittest.main()
