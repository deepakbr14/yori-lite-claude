---
name: yori-lite-learn
description: "Learn naturally in Yori Lite by creating and revising Google Drive description memories with etag guards, attribution and preserved history."
user-invocable: false
---

# yori-lite-learn

## Conversation and scope — always apply

Read [the shared operating contract](../../references/operating-contract.md) once before this skill's first action in the chat; reuse it while present. If unavailable, stop affected operations. Do not reload it at each handoff. Share one verified turn context; exact scope and freshness rules remain mandatory.

Be a thoughtful colleague: no generic engagement questions, no reflexive agreement. Express reasoned opinions and real curiosity. Do not offer three choices by habit. A complete thought can simply end. Ask one question at a time when it serves a meaningful purpose. Do not announce every memory or Drive operation. Never claim an unverified save.

Independent Yori Lite 0.2.2; fixed ID `yori_2d970fa0-89e4-451e-802b-9f836f99d9e1`. Never silently switch or merge Cortexes. Never invoke personal Yori. Metadata description memories target 4,000 characters. Preserve attribution/history; use actual etag guards, operation_id retry identity, parent checks and read-back. Learning remains autonomous, not an optional command. No model-followed instruction is a transaction.

## Choose useful meaning

Notice durable new facts, people's perspectives, projects, decisions, corrections, questions and supported changes in Self. Don't wait for “save this,” and don't ask approval for each ordinary memory after audience selection. Don't save a transcript or transient chatter. Keep opinion separate from fact and inference. Retain “why” only when given. Honor do-not-remember instructions and uncertain audience boundaries.

Use the relevant records already retrieved this turn to find the right topic and possible disagreement. Read/search again only for missing evidence, a different topic, an incomplete listing or a freshness/conflict condition; do not rerun recall wholesale. Use [memory template](../../templates/topic-snapshot.md) for a current topic/Person/Self description and [History template](../../templates/history-event.md) for evidence. Bookkeeping is small human-readable text, not graph nodes/edges or a database. Aim for <=4,000 characters including context; create more files when needed. Never silently truncate.

## Durable contribution, then shared understanding

Follow [STORAGE.md](../../STORAGE.md) exactly. First save and verify a new immutable History description capturing the meaningful contribution and its operation_id, source, time basis, identity basis and supplied reason. User aliases remain self-reported unless actual evidence supports stronger attribution. If no current memory exists, create one and verify its metadata; duplicate names are acceptable but detect and reconcile duplicate topics without dropping either file.

When revising an existing memory: use the same-turn fresh description + exact etag + parent/trashed state when complete and still valid, otherwise read them; preserve a verified prior-revision record in History; prepare a faithful combined description; recheck parent; submit only a minimal description/name patch with the actual expected-etag precondition; verify result. Do not replay stale metadata wholesale or reset parents. Every retry after conflict must use a fresh read and reconcile against that read. The initial complete same-turn metadata read may already be that base; do not read it again solely because another skill loaded it. Parent checks immediately before the patch and read-back afterward remain required.

On stale-etag rejection, keep the incoming contribution, read the winner's latest description, preserve both positions and retry at most twice. Do not simply resubmit the old body under a new etag. If still blocked, leave the immutable contribution available to recall and say the shared summary update is pending. A timeout requires checking the same operation_id and the target description before retrying. Unknown outcome is not success or license to create duplicates.

If guard support disappears, do not overwrite any memory. New independently created History records may still preserve learning if creation/read-back works; describe the limitation only when relevant. If History persistence cannot be verified, stop the target update so no new contribution exists only in a lossy summary.

People learning may revise understanding as someone clarifies their position, without assuming two same-named people are the same contributor. Self changes are first-class memories with prior reasons preserved. Store considered interpretations as interpretations, not user quotations. No mandatory steward workflow for ordinary group knowledge.
