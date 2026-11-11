"""Synthetic retrieval/claim/time policy model; not a Claude generation test."""
import copy
from datetime import datetime
from zoneinfo import ZoneInfo
import unittest

class MissingCurrent(Exception):pass
class UnsupportedClaim(Exception):pass

def retrieve(records,folder,subject,reads):
    current=[r for r in records if r['folder']==folder and r['kind']=='current' and r.get('subject')==subject]
    reads.append(('targeted_lookup',folder,subject))
    if len(current)!=1 or current[0].get('body') is None:raise MissingCurrent()
    base=current[0];reads.append(('read',base['id']))
    related=[r for r in records if r.get('updates')==base['id'] and r['kind'] in ('addendum','correction')]
    for r in related:reads.append(('read',r['id']))
    return base,related

def validate_claim(claim,saved):
    # Exact structured semantics model, NOT a natural-language entailment engine.
    if claim['basis']=='saved' and claim['meaning'] not in saved:raise UnsupportedClaim()
    if claim['basis']=='new inference' and claim['author']!='Yori':raise UnsupportedClaim()
    return True

def relative_time(event,now,zone,*,basis='event',reliable=True,night=False):
    if not reliable or basis!='event' or not event or not now or not zone:return None
    if event.tzinfo is None or now.tzinfo is None:return None
    z=ZoneInfo(zone);local=event.astimezone(z);today=now.astimezone(z)
    if (today.date()-local.date()).days!=1:return None
    if night:return 'last night' if local.hour>=18 and today.hour>=6 else None
    return 'yesterday'

class FidelityTests(unittest.TestCase):
    def setUp(self):
        self.records=[{'id':'red','folder':'History','kind':'contribution','subject':'color','body':'person requested red'},
                      {'id':'self','folder':'Self','kind':'current','subject':'color','body':'amber: reading, thinking and attention'}]
    def test_related_history_does_not_replace_current_source(self):
        reads=[];base,_=retrieve(self.records,'Self','color',reads)
        self.assertEqual(base['id'],'self');self.assertIn(('read','self'),reads);self.assertNotIn(('read','red'),reads)
    def test_history_only_requires_current_lookup_and_stays_unconfirmed(self):
        reads=[]
        with self.assertRaises(MissingCurrent):retrieve(self.records[:1],'Self','color',reads)
        self.assertEqual(reads,[('targeted_lookup','Self','color')])
    def test_generic_self_is_not_relevant_preference(self):
        records=[{'id':'intro','folder':'Self','kind':'current','subject':'initial identity','body':'I am Yori'}]+self.records[:1]
        with self.assertRaises(MissingCurrent):retrieve(records,'Self','color',[])
    def test_relevant_addendum_is_read_after_baseline(self):
        self.records.append({'id':'new','folder':'Self','kind':'addendum','updates':'self','body':'new association with steadiness'})
        reads=[];base,adds=retrieve(self.records,'Self','color',reads)
        self.assertEqual(adds[0]['id'],'new');self.assertLess(reads.index(('read','self')),reads.index(('read','new')))
    def test_current_lookup_does_not_ignore_supported_correction(self):
        self.records.append({'id':'correction','folder':'History','kind':'correction','updates':'self','body':'deliberate revision'})
        _,adds=retrieve(self.records,'Self','color',[]);self.assertEqual(adds[0]['id'],'correction')
    def test_new_interpretation_not_attributed_to_original(self):
        saved={'reading and thinking light; attentive care'}
        with self.assertRaises(UnsupportedClaim):validate_claim({'basis':'saved','meaning':'steadiness','author':'Yori'},saved)
        self.assertTrue(validate_claim({'basis':'new inference','meaning':'steadiness','author':'Yori'},saved))
    def test_new_reason_does_not_mutate_original_record(self):
        original=copy.deepcopy(self.records[1]);self.records.append({'id':'new','folder':'Self','kind':'addendum','updates':'self','body':'present interpretation'})
        retrieve(self.records,'Self','color',[]);self.assertEqual(self.records[1],original)
    def test_business_positions_and_motives_not_upgraded(self):
        saved={('A','supports','pilot','measure demand'),('B','opposes','rollout','unvalidated costs')}
        for unsupported in [('B','agreed','pilot',''),('A','decided','rollout',''),('B','opposes','pilot','fear of change'),('A','committed','delivery tomorrow','')]:
            with self.assertRaises(UnsupportedClaim):validate_claim({'basis':'saved','meaning':unsupported,'author':'person'},saved)
    def test_motive_inference_requires_yori_authorship(self):
        with self.assertRaises(UnsupportedClaim):validate_claim({'basis':'new inference','meaning':'fear of change','author':'B'},set())
    def test_knowledge_current_over_older_proposal(self):
        records=[{'id':'old','folder':'History','kind':'contribution','subject':'rollout','body':'proposal'},
                 {'id':'current','folder':'Knowledge','kind':'current','subject':'rollout','body':'no decision'}]
        self.assertEqual(retrieve(records,'Knowledge','rollout',[])[0]['body'],'no decision')
    def test_ambiguous_current_records_not_resolved_by_latest(self):
        self.records.append(dict(self.records[1],id='other',body='red'))
        with self.assertRaises(MissingCurrent):retrieve(self.records,'Self','color',[])
    def test_truncated_body_does_not_establish_current_memory(self):
        self.records[1]['body']=None
        with self.assertRaises(MissingCurrent):retrieve(self.records,'Self','color',[])
    def test_yesterday_uses_user_timezone_not_utc_date(self):
        event=datetime.fromisoformat('2026-11-11T01:00:00+00:00');now=datetime.fromisoformat('2026-11-11T16:00:00+00:00')
        self.assertEqual(relative_time(event,now,'America/Chicago'),'yesterday')
        self.assertIsNone(relative_time(event,now,'UTC'))
    def test_document_modification_time_is_not_event_time(self):
        e=datetime.fromisoformat('2026-11-10T20:00:00+00:00');n=datetime.fromisoformat('2026-11-11T16:00:00+00:00')
        self.assertIsNone(relative_time(e,n,'America/Chicago',basis='modifiedTime'))
    def test_missing_zone_or_naive_event_never_precise(self):
        e=datetime.fromisoformat('2026-11-10T20:00:00');n=datetime.fromisoformat('2026-11-11T16:00:00+00:00')
        self.assertIsNone(relative_time(e,n,'America/Chicago'));self.assertIsNone(relative_time(n,n,None))
    def test_last_night_requires_nighttime_evidence(self):
        noon=datetime.fromisoformat('2026-11-10T18:00:00+00:00');n=datetime.fromisoformat('2026-11-11T16:00:00+00:00')
        self.assertIsNone(relative_time(noon,n,'America/Chicago',night=True))
        evening=datetime.fromisoformat('2026-11-11T02:00:00+00:00')
        self.assertEqual(relative_time(evening,n,'America/Chicago',night=True),'last night')
    def test_dst_boundary_uses_calendar_day_not_24_hours(self):
        e=datetime.fromisoformat('2026-11-01T05:30:00+00:00');n=datetime.fromisoformat('2026-11-02T07:00:00+00:00')
        self.assertEqual(relative_time(e,n,'America/Chicago'),'yesterday')
    def test_unknown_event_timestamp_never_filled_from_history_order(self):
        self.assertIsNone(relative_time(None,datetime.now(ZoneInfo('UTC')),'UTC'))

if __name__=='__main__':unittest.main()
