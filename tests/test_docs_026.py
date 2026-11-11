"""Local fault model of Docs storage/migration; no network or live Claude execution.
Models conditional writes and authority boundaries, not prose interpretation or API syntax.
"""
import copy
import unittest
import uuid

class Blocked(Exception): pass
class Conflict(Exception): pass

class Docs:
    def __init__(self,guard=True):
        self.guard=guard;self.files={};self.receipts={};self.pending={};self.fail_snapshot=False
    def create(self,body,parent,kind='memory',**meta):
        key=str(uuid.uuid4());self.files[key]=dict(body=body,parent=parent,kind=kind,rev=1,**meta)
        return key
    def read(self,key):return copy.deepcopy(self.files[key])
    def patch(self,key,body,rev):
        f=self.files[key]
        if f['parent']=='History' and f['body']:raise Blocked('immutable History')
        if not self.guard:raise Blocked('no strict guard')
        if f['rev']!=rev:raise Conflict()
        f.update(body=body,rev=rev+1)
    def revise(self,key,body,before_write=None):
        base=self.read(key)
        contribution=self.create(body,'History','contribution')
        assert self.read(contribution)['body']==body
        snap=self.create(base['body'],'History','prior',source=key,source_rev=base['rev'],contribution=contribution)
        if self.fail_snapshot:raise Blocked('unverified snapshot')
        assert self.read(snap)['body']==base['body']
        if before_write:before_write()
        if self.read(key)['parent']!=base['parent']:raise Blocked('moved')
        if self.guard:
            self.patch(key,body,base['rev']);assert self.read(key)['body']==body;return key
        add=self.create(body,base['parent'],'addendum',updates=key,contribution=contribution,prior=snap)
        assert self.read(add)['body']==body;return add
    def recall(self,key):
        return [self.read(key)['body']]+[f['body'] for f in self.files.values() if f.get('updates')==key and f['parent']==self.files[key]['parent']]
    def migrate(self,key,interrupt=None):
        source=self.read(key)
        if 'description' not in source or source['description'] is None:raise Blocked('source unknown')
        raw=source['description']
        if key in self.receipts:
            old,dest=self.receipts[key]
            if old!=raw:raise Conflict('legacy source changed')
            return dest  # never replay stale source over later body learning
        candidates=[k for k,f in self.files.items() if f.get('legacy_source')==key]
        if len(candidates)>1:raise Conflict('duplicate migration candidates')
        evidence=[k for k,f in self.files.items() if f.get('evidence_source')==key and f['body']==raw]
        if len(evidence)>1:raise Conflict('duplicate evidence')
        ev=evidence[0] if evidence else self.create(raw,'History','migration evidence',evidence_source=key)
        assert self.read(ev)['body']==raw
        body='# Remembered information\n\n'+raw+'\n\nYori memory format: 2'
        if candidates:
            dest=candidates[0]
            if self.files[dest]['body']!=body:raise Conflict('candidate differs')
        elif key in self.pending:
            dest=self.pending[key]
            if self.files[dest]['body']!=body:raise Conflict('partial body differs')
        else:
            if source['body']:raise Conflict('pre-existing meaningful body')
            if self.guard:
                self.patch(key,body,source['rev']);dest=key;self.pending[key]=dest
            else:
                dest=self.create(body,source['parent'],legacy_source=key,evidence=ev);self.pending[key]=dest
        if interrupt=='after_body':raise Blocked('lost completion receipt')
        if self.files[key]['description']!=raw:raise Conflict('source changed during copy')
        assert self.read(dest)['body']==body
        receipt=self.create('Verified migration','History','migration complete',source=key,destination=dest,evidence=ev)
        self.read(receipt);self.receipts[key]=(raw,dest)
        return dest

class DocsProtocolTests(unittest.TestCase):
    def test_new_body_is_readable_and_description_not_primary(self):
        d=Docs();key=d.create('# Favorite color\n\nAmber, for warmth.','Self')
        self.assertIn('Amber',d.read(key)['body']);self.assertNotIn('description',d.read(key))
    def test_guarded_change_snapshots_exact_prior(self):
        d=Docs();key=d.create('# Color\n\nAmber — original reason.','Self');old=d.read(key)
        d.revise(key,'# Color\n\nRed — temporary choice.')
        self.assertTrue(any(f['kind']=='prior' and f['body']==old['body'] for f in d.files.values()))
    def test_missing_guard_keeps_learning_without_replacement(self):
        d=Docs(False);key=d.create('# Color\n\nAmber','Self');old=d.read(key)
        add=d.revise(key,'# Updated choice\n\nRed, temporarily.')
        self.assertEqual(d.read(key),old);self.assertEqual(d.read(add)['updates'],key)
        fresh=copy.deepcopy(d);self.assertEqual(len(fresh.recall(key)),2)
    def test_two_guard_free_contributors_both_survive(self):
        d=Docs(False);key=d.create('# People\n\nDistinct speakers','People')
        a=d.revise(key,'Person A prefers blue');b=d.revise(key,'Person B prefers green')
        self.assertNotEqual(a,b);self.assertIn('Person A prefers blue',d.recall(key));self.assertIn('Person B prefers green',d.recall(key))
    def test_guard_conflict_preserves_contribution_and_winner(self):
        d=Docs();key=d.create('amber','Self')
        with self.assertRaises(Conflict):d.revise(key,'red',lambda:d.patch(key,'green',1))
        self.assertEqual(d.read(key)['body'],'green')
        self.assertTrue(any(f['kind']=='contribution' and f['body']=='red' for f in d.files.values()))
    def test_unverified_snapshot_blocks_guarded_change(self):
        d=Docs();key=d.create('amber','Self');d.fail_snapshot=True
        with self.assertRaises(Blocked):d.revise(key,'red')
        self.assertEqual(d.read(key)['body'],'amber')
    def test_history_cannot_be_corrected_in_place(self):
        d=Docs();key=d.create('Yori inferred a test; uncertain','History','contribution')
        with self.assertRaises(Blocked):d.patch(key,'Person explicitly said test',1)
    def test_same_doc_migration_preserves_id_and_source(self):
        d=Docs();key=d.create('','Self',description='Amber; reason: warmth.')
        self.assertEqual(d.migrate(key),key);self.assertEqual(d.read(key)['description'],'Amber; reason: warmth.')
    def test_guard_free_mirror_preserves_logical_identity(self):
        d=Docs(False);key=d.create('','People',description='Preferred name supplied by speaker.')
        dest=d.migrate(key);self.assertNotEqual(dest,key);self.assertEqual(d.read(dest)['legacy_source'],key)
        self.assertEqual(d.read(key)['body'],'');self.assertEqual(d.read(dest)['parent'],'People')
    def test_retry_after_body_reuses_candidate_and_evidence(self):
        for guard in [False,True]:
            d=Docs(guard);key=d.create('','Self',description='amber')
            with self.assertRaises(Blocked):d.migrate(key,interrupt='after_body')
            n=len(d.files);dest=d.migrate(key);self.assertEqual(len(d.files),n+1)
            n=len(d.files);self.assertEqual(d.migrate(key),dest);self.assertEqual(len(d.files),n)
    def test_resume_never_overwrites_later_docs_learning(self):
        d=Docs();key=d.create('','Self',description='amber');d.migrate(key);d.revise(key,'red with context')
        self.assertEqual(d.migrate(key),key);self.assertEqual(d.read(key)['body'],'red with context')
    def test_nonempty_body_conflict_preserves_both(self):
        d=Docs();key=d.create('user-authored body','Self',description='legacy source')
        with self.assertRaises(Conflict):d.migrate(key)
        self.assertEqual(d.read(key)['body'],'user-authored body');self.assertEqual(d.read(key)['description'],'legacy source')
    def test_missing_description_is_not_empty(self):
        d=Docs();key=d.create('','Self')
        with self.assertRaises(Blocked):d.migrate(key)
        self.assertEqual(len(d.files),1)
    def test_duplicate_mirrors_stop_authority(self):
        d=Docs(False);key=d.create('','People',description='a name')
        d.create('a','People',legacy_source=key);d.create('b','People',legacy_source=key)
        with self.assertRaises(Conflict):d.migrate(key)
        self.assertNotIn(key,d.receipts)
    def test_source_changed_after_completion_is_not_replayed(self):
        d=Docs();key=d.create('','Self',description='amber');d.migrate(key);body=d.read(key)['body']
        d.files[key]['description']='later legacy edit'
        with self.assertRaises(Conflict):d.migrate(key)
        self.assertEqual(d.read(key)['body'],body)

if __name__=='__main__':unittest.main()
