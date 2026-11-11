"""Local recognition-policy model. Not Claude behavior or an authentication service.
Only synthetic account keys/participants; no private tool result values are fixtures.
"""
from dataclasses import dataclass
import unittest

@dataclass(frozen=True)
class Signal:
    provider:str
    namespace:str
    field:str
    value:str
    email:str=''
    def key(self):return (self.provider,self.namespace,self.field,self.value)

@dataclass(frozen=True)
class Result:
    person:str|None
    basis:str
    ask:bool
    personal_history:bool

def resolve(participants,bindings=(),signal=None,*,complete=True,explicit=None,
            guest=False,shared_key=False,needs_person=False,sensitive=False):
    # Participants are logical IDs of direct participants, not all People docs.
    ids=set(participants)
    if guest:return Result(None,'unknown speaker',needs_person,False)
    if explicit is not None:return Result(explicit,'self-reported/contextual',False,True)
    mapped=set()
    contrary=False
    if signal:
        relevant=[b for b in bindings if b['active'] and b['provider_key'][:3]==signal.key()[:3]]
        mapped={b['person'] for b in relevant if b['provider_key']==signal.key() and b['grounded']}
        contrary=bool(relevant) and not mapped
    if len(mapped)==1 and not shared_key:
        return Result(next(iter(mapped)),'authenticated account; contextual person link',False,True)
    if len(mapped)>1 or shared_key or contrary:
        return Result(None,'ambiguous account association',needs_person,False)
    if complete and len(ids)==1:
        if sensitive:return Result(None,'default insufficient for sensitive request',True,False)
        return Result(next(iter(ids)),'sole-participant default',False,needs_person)
    return Result(None,'unresolved',needs_person,False)

def bind(bindings,signal,person,basis):
    if signal is None or basis not in ('explicit linkage','verified prior linkage'):
        raise ValueError('no grounded account/person association')
    candidate=dict(provider_key=signal.key(),person=person,grounded=True,active=True)
    if candidate not in bindings:bindings.append(candidate)

class IdentityPolicyTests(unittest.TestCase):
    def setUp(self):
        self.google=Signal('google','connector-A','subject','synthetic-account-A')
        self.bindings=[]
    def test_personal_single_participant_no_identifier(self):
        r=resolve(['person-A']);self.assertEqual(r.person,'person-A');self.assertFalse(r.ask)
        self.assertEqual(r.basis,'sole-participant default');self.assertFalse(r.personal_history)
    def test_returning_person_reuses_grounded_mapping(self):
        bind(self.bindings,self.google,'person-A','explicit linkage')
        r=resolve(['person-A','person-B'],list(self.bindings),self.google)
        self.assertEqual(r.person,'person-A');self.assertFalse(r.ask)
        self.assertEqual(len(self.bindings),1)
    def test_two_shared_participants_generic_greeting_no_question_or_history(self):
        r=resolve(['person-A','person-B']);self.assertIsNone(r.person)
        self.assertFalse(r.ask);self.assertFalse(r.personal_history)
    def test_shared_personal_recall_requires_question_before_history(self):
        r=resolve(['person-A','person-B'],needs_person=True)
        self.assertTrue(r.ask);self.assertFalse(r.personal_history)
    def test_unknown_guest_overrides_account_and_default(self):
        bind(self.bindings,self.google,'person-A','explicit linkage')
        r=resolve(['person-A'],self.bindings,self.google,guest=True,needs_person=True)
        self.assertIsNone(r.person);self.assertTrue(r.ask);self.assertFalse(r.personal_history)
    def test_failed_profile_same_as_unavailable_for_personal_default(self):
        r=resolve(['person-A'],signal=None);self.assertEqual(r.person,'person-A');self.assertFalse(r.ask)
    def test_names_and_mentions_are_not_counted_as_distinct_participant_files(self):
        r=resolve(['person-A','person-A']) # mirror/addendum already resolve to logical ID
        self.assertEqual(r.person,'person-A');self.assertFalse(r.ask)
    def test_default_cannot_create_authenticated_mapping(self):
        with self.assertRaises(ValueError):bind(self.bindings,self.google,'person-A','sole-participant default')
        self.assertEqual(self.bindings,[])
    def test_same_account_shared_by_two_people_is_ambiguous(self):
        bind(self.bindings,self.google,'person-A','explicit linkage')
        bind(self.bindings,self.google,'person-B','explicit linkage')
        r=resolve(['person-A','person-B'],self.bindings,self.google,needs_person=True)
        self.assertIsNone(r.person);self.assertTrue(r.ask);self.assertFalse(r.personal_history)
    def test_signal_namespace_provider_and_field_must_match(self):
        bind(self.bindings,self.google,'person-A','explicit linkage')
        for signal in [Signal('claude','connector-A','subject','synthetic-account-A'),
                       Signal('google','other-scope','subject','synthetic-account-A'),
                       Signal('google','connector-A','email','synthetic-account-A')]:
            r=resolve(['person-A','person-B'],self.bindings,signal,needs_person=True)
            self.assertIsNone(r.person);self.assertTrue(r.ask)
    def test_different_known_account_does_not_use_old_default(self):
        bind(self.bindings,self.google,'person-A','explicit linkage')
        other=Signal('google','connector-A','subject','synthetic-account-B')
        r=resolve(['person-A'],self.bindings,other,needs_person=True)
        self.assertIsNone(r.person);self.assertFalse(r.personal_history)
    def test_same_id_changed_email_keeps_person(self):
        bind(self.bindings,self.google,'person-A','explicit linkage')
        changed=Signal('google','connector-A','subject','synthetic-account-A','new@example.invalid')
        self.assertEqual(resolve(['person-A','person-B'],self.bindings,changed).person,'person-A')
    def test_incomplete_inventory_cannot_assert_sole_participant(self):
        r=resolve(['person-A'],complete=False,needs_person=True)
        self.assertIsNone(r.person);self.assertTrue(r.ask)
    def test_mapping_reuse_no_duplicate_binding(self):
        bind(self.bindings,self.google,'person-A','explicit linkage')
        bind(self.bindings,self.google,'person-A','verified prior linkage')
        self.assertEqual(len(self.bindings),1)
    def test_explicit_identification_overrides_contextual_default(self):
        r=resolve(['person-A'],explicit='person-B');self.assertEqual(r.person,'person-B')
        self.assertEqual(r.basis,'self-reported/contextual')
    def test_sensitive_history_not_revealed_on_default(self):
        r=resolve(['person-A'],needs_person=True,sensitive=True)
        self.assertTrue(r.ask);self.assertFalse(r.personal_history)
    def test_shared_key_not_silently_rebound(self):
        bind(self.bindings,self.google,'person-A','explicit linkage')
        r=resolve(['person-A'],self.bindings,self.google,shared_key=True)
        self.assertIsNone(r.person);self.assertEqual(len(self.bindings),1)

if __name__=='__main__':unittest.main()
