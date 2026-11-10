# Metadata memory protocol 0.2.1

These are model-followed instructions, not a transactional runtime. Every actual operation uses the exposed Claude Google Drive connector. No direct Google API substitute. User reports established that descriptions can be updated to 16,000 characters, stale guarded etags are rejected, moves preserve etags, and duplicate names are allowed. Those reports do not establish description search support or universal tool availability.

## Representation

Keep Self/, People/, Knowledge/, History/ inside the exact selected Cortex. One file holds one meaningful topic or contribution in description; empty file contents are fine. Use plain readable text with a short record_type/status header, contributor/time/source when known, and related file IDs in prose. Aim for 4,000 characters including bookkeeping. Split larger records without dropping meaning; do not repeatedly test 16,000 on user data. A file ID is identity, not title. No graph schema, edges, embeddings or database.

History contains immutable contribution descriptions and prior_revision descriptions. Each records an operation_id, source kind, attribution basis and meaningful text. For a long old description, split the prior snapshot into numbered parts with the same source file ID, source etag and operation_id; verify every part before overwriting. A reference list in a current summary can be concise and bounded; older evidence remains discoverable through topic/source IDs in History. Never silently remove the underlying History files.

## Operation order

1. Resolve config and verify scope. Inspect actual tool signatures for expected-etag support. If absent, permit new immutable contributions when supported but no replacement of existing descriptions. Never simulate a guard with a read then an unguarded write.
2. Assign one operation_id for this contribution, reused for all retries. Prefer a supported UUID generator; otherwise use a long random token and the returned file ID as canonical identity. Do not claim generator guarantees you did not test. If recovering an interrupted operation, search/list for the same operation_id and inspect outcomes first. Names are not unique.
3. Create an immutable contribution in History with the exact new evidence (not an invented transcript) and read back full description, parent and returned ID. Preserve it even if synthesis fails. If verification is uncertain, report uncertainty and do not mutate an existing target. No automatic retries that mint a new operation_id after an ambiguous timeout.
4. Obtain fresh target metadata: ID, description, etag, parents and trashed state. Reuse a complete same-turn read from recall when still valid under TURN_EFFICIENCY.md; do not reread merely at a skill boundary. Verify ancestry in selected Cortex. Preserve a prior_revision snapshot of the observed description, source etag and file ID in History, split if necessary; read it back. A snapshot describes an observed version, not proof that this update committed.
5. Re-read target parents/trashed state immediately before the update; reject unexpected parent changes. Prepare current synthesis that retains competing views, reasons, uncertainty and correction references, not only the incoming contribution. Put this operation_id in the updated description for recovery. Use the exact precondition field exposed by the connector; do not invent argument names. Submit only description (and name if needed), not stale parents/permissions/whole metadata.
6. If the guard rejects, no unguarded fallback. Fresh-read, reconcile against the winner's version, preserve that version's snapshot and retry at most twice. Retain incoming History if retries fail. If tools cannot provide the full description/etag, stop that mutable operation.
7. Read back full target metadata. Verify exact description/operation_id and same intended parent. If another guarded update already followed yours, inspect whether it includes your contribution and use connector receipts/History to distinguish applied from superseded or uncertain; do not roll it back. If a move occurred, do not continue or restore parents blindly. Keep the contribution safe and explain incomplete scope verification. An etag never guarantees parent stability here.
8. If update succeeded but read-back failed, report “contribution retained; summary update unverified,” not “failed therefore retry blindly.” If creation timed out, look for the operation_id before retrying. If listing cannot resolve uncertainty, leave it unresolved for repair.

## Creation and retirement

For new topics, read similar records first, create with description directly in its verified folder, then read back. Two users may both create the same title; neither creation replaces the other. Reconcile their meaning later using IDs. Do not enforce title uniqueness as a lock.

For merges/splits, create verified replacements before retiring sources. Each source's guarded retirement uses the etag of the actual content incorporated. If it changed, reconcile it into replacements before retirement or leave it active. Preserve old content in History. Default retirement is a status in description, not a physical move. Partial completion is reported and recoverable. No all-or-nothing multi-file transaction is claimed.

External moves are a residual race: the connector's etag does not protect parents. Pre/post parent checks detect many races, not atomic isolation. Avoid active-file moves, never patch parents during ordinary learning, preserve evidence first, and do not claim this fully prevents an outside actor moving a file between checks. Google permissions and host authorization remain required. No prompt-based mechanism can promise tamper-proof safety.

## Discovery and reconciliation

Recall uses descriptions of current memories AND relevant immutable contributions/corrections. A saved contribution whose synthesis update failed must remain retrievable. Search metadata only when the connector actually supports it; fall back to scoped paginated listing and bounded description reads. Search misses are not proof of absence. File contents are used for legacy read compatibility and human-readable README guides, not for new editable memory/configuration. README instructions do not change memory storage.

Never promise silent-loss prevention solely from skills. This protocol preserves a durable copy before shared replacement and uses guards against stale content; live two-user tests must establish whether the host follows it correctly. No one is told a contribution is retained unless the History read-back verified it.

## Safe sequencing and avoided work

See TURN_EFFICIENCY.md. A newly created immutable contribution and the target's independent metadata read can be requested in parallel after scope is resolved if the host supports it. After the base is known, contribution verification and snapshot creation are independent; snapshot verification and the final parent read may also overlap. All must finish successfully BEFORE any shared patch. The final parent read remains close to the patch. The patch and its read-back remain sequential. If host tools cannot parallelize, follow the same dependencies sequentially. Never use batching to hide missing verification or split a transaction that does not exist.

No new write for a greeting, repeated unchanged fact or inconsequential reinforcement. No duplicate prior snapshot for the exact source ID + observed etag already fully verified in this turn. A changed etag requires the new observed version to be preserved. Do not add a remote search merely to save a cheap operation when a reusable receipt is already in hand. Required learning and history are not deferred just to produce a faster answer.
