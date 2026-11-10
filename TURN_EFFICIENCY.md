# Turn efficiency without weaker memory

This is a scheduling guide for the Skills, not an executable runtime or latency promise.

## Share current evidence

Fresh chat: resolve config through the convention and load the selected Cortex from Drive. Inside that turn, keep one context with exact config/Cortex/subfolder IDs, relevant tool capability definitions, completed paginated searches, records with description/etag/parents, operation IDs and verified write receipts. Pass that context between skills. Do not rediscover the registry, reload Self, inspect tools, or redo identical queries for each skill.

Later turns in the SAME chat may address previously resolved IDs directly instead of searching by name again. Before the first Cortex operation in a later turn, validate the config by its known ID (and parent/owner) and selected folder access; do not repeat this check at every skill boundary. A fresh chat still discovers the pointer anew. Missing permissions, an account change, different config/target, an incomplete result, a move or an unexpected revision invalidates affected context; stop or re-resolve rather than silently switching. Never persist this cache in another store or infer current content from a prior chat.

Only use a retrieved description as the initial update base when it includes the full description, exact etag and verified ancestry from this turn and has not been invalidated. If there has been an intervening user message/pause, a failed operation, known change or incomplete response, obtain a fresh read. Keep the immediate pre-update parent/trashed check and post-update full metadata read-back. A stale etag still causes a fresh-read reconcile, not blind retry. These rules do not claim parent isolation against external moves.

## Scheduling with preserved dependencies

For one shared revision after discovery, without reuse, the existing protocol has eight essential calls:

1. create contribution
2. verify contribution by read-back
3. read target base
4. create prior snapshot
5. verify snapshot by read-back
6. check target parent/trashed state
7. guarded patch
8. read back target

The prior simple serial schedule is 8 dependent waiting stages when executed literally. The same eight calls can take 5 waiting stages IF the actual host supports independent calls in parallel: (create contribution + read base), (verify contribution + create snapshot), (verify snapshot + parent check), guarded patch, target read-back. Reusing a complete same-turn base avoids its duplicate get entirely. All evidence verification and parent checking are hard prerequisites of the patch. Multiple snapshot parts add operations; conflicts and network failures add retries. These are static call/dependency counts, NOT measured Google latency or a guaranteed speedup.

Do not parallelize dependent writes, patches with their snapshots, or a write with its read-back. Never omit a guard or a required read-back to meet a call budget. Use returned metadata to avoid duplicate gets only for discovery/initial bases when complete; creates and writes still have their required read-backs. Do not rerun setup probes or README repairs during ordinary learning.

## Retrieval and writes

Reuse a completed same-turn scoped query and its descriptions. Search again for a different subject, missing fields, explicit new evidence, incomplete pagination or relevant changes; a cached miss is not permanent. No blanket full-Cortex scan or reload for a small learning update. Keep bounded retrieval plus relevant pending History contributions. If a meaningful claim is unchanged, avoid manufacturing another event; a new reason, correction or dissent remains worth preserving.

Do not announce internal work just to fill a pause. Complete warranted learning in the current turn. A no-op learning decision is not a reason to ask an engagement question.

## Latency evidence

The user reported about 35 seconds for the fictional Aurora conversation in 0.2.0. No tool trace or per-call durations were supplied, so the cause and possible seconds saved are unknown. Local test duration measures developer tests only, never Claude/Drive response time.

For a disposable live comparison, record client/version, fresh vs warm chat, user-send time, final response time, available connector start/end times, call names/counts, retries, and required learn/read-back outcomes. Use the same dummy task on equivalent fresh folders; distinguish setup from ordinary learning. Record at least three runs per condition if practical, report observed median/range without inventing unavailable call times. Do not put account IDs or real memory into the public report. tests/LATENCY_LOG.md is the template.
