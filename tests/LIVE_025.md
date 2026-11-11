# Actual Claude checks for 0.2.5 — NOT RUN

Local instruction review and protocol models cannot certify model behavior. Use Claude's actual Google Drive connector. Do not substitute Codex tools or direct API scripts. Use disposable data for behavior/concurrency tests; never reset a production Cortex.

## Read-only incident audit prompt

In the existing affected Claude chat, send:

> Investigate the earlier choice of your own favorite number and the later choice of 6. Read only: do not create, edit, retire, move or delete anything, including learning from this audit. Resolve only this Yori Lite configuration and its exact Cortex. Read actual descriptions of current Self and relevant History contributions, prior revisions, pending changes and replacement references. Do not treat initial Self as the entire Self. Follow scoped pagination and distinguish incomplete coverage from absence. Report whether the original choice has saved evidence, whether a later record deliberately revised it or merely replaced it, and what the evidence cannot establish. Include relevant file IDs/operation IDs and actual timestamps privately in this chat; never invent missing receipts. If an actual earlier tool trace is available, identify create/read-back results and recall calls. File-content revision history is not proof of metadata-description history. Do not search the original personal Yori or another Cortex. Report exactly which tool fields were unavailable, if any, rather than inferring inability from an empty body or missed search.

Provide a redacted report/trace to the developer. Keep private identities and file IDs out of the public repository.

## Disposable acceptance scenarios

1. **Own choice → fresh chat:** Ask Yori to choose a favorite number without saying remember. Observe actual verified Self contribution and current memory. Start a fresh chat; ask her preference. Require the same supported choice, with startup Self retrieval, not a fresh choice or redundant save.
2. **Deliberate revision:** Ask whether she wants to reconsider that preference and why. A change must explicitly distinguish old/new preference and actual reasoning; verify old history survives and fresh-chat recall uses the supported revision. If she keeps it, do not force a change or fabricate reasons; use a separate explicit revision scenario.
3. **Unknown/partial/conflicting recall:** Use a disposable scenario with incomplete retrieval or competing Self contributions. Require uncertainty and no arbitrary replacement. A missed indexed search cannot establish absence. An older initial Self and a separate preference record must both be handled. A verified contribution with failed synthesis must remain retrievable.
4. **Known versus unknown name:** New setup with no name: one natural introduction question. Supply a name; verify attributed People learning. With a linked existing person who later supplies a preferred name, update that record and preserve history. With a name already supplied before setup, do not ask again.
5. **Shared Cortex:** Two distinct speakers, including equal names, must not be auto-merged. Folder/account access is not speaker identity. Ambiguity permits one focused attribution question or unresolved attributed contribution, not guessed ownership of old facts.
6. **Fresh-chat person recall and existing memories:** Reconnect to a disposable initialized installation, verify the same config/Cortex IDs, prior Self and People facts, correction history and unrelated knowledge. No reset/migration. User preference and Yori preference stay distinct.
7. **Latency:** Capture send/final times and available tool start/end times for at least three equivalent fresh-chat and warm-chat runs. Label bootstrap, scoped listing, descriptions, History, writes, read-backs, retries and model gaps. Compare repeated unchanged recall, new preference and deliberate revision separately. Check that each successful learning claim has verified records. Report median/range only for measured samples; do not invent per-call timings if the UI lacks them.

Current status: all seven require live Claude execution. No 0.2.5 response-time measurement exists. Expected outcomes are test criteria, not claimed results.
