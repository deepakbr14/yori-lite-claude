# Real Google Docs source test — 0.2.8

Executed through **Codex's Google Drive/Docs connector**, not Claude. Created a new disposable root with Self, People, Knowledge and History. No active config was repointed, no production/personal Yori file was read or changed, and the prior experimental Cortex was untouched. This is an unregistered source fixture, not a completed plugin onboarding or fresh-Claude test.

Eight native Docs were created, placed while empty, initialized with requiredRevisionId using the exposed connector parameter, then read back and compared exactly to the authored synthetic contents:

- History: original amber reason; separate red request; older business rollout proposal.
- Self: current amber preference with the original reading/thinking/attention reason; separate present steadiness interpretation.
- People: two distinct synthetic participants with different explicit positions/reasons.
- Knowledge: current pilot/rollout status, with no final agreement, owner, deadline or outcome.

Actual subsequent retrieval intentionally began with the misleading red History entry, then a scoped search in Self resolved the current preference, followed by actual current-body and addendum reads. The body preserved the original reason and kept steadiness explicitly new. Business current/People/history bodies were reread and compared with saved contents. Original amber History was also reread unchanged. These are source/read-back assertions, not a generated-answer benchmark. No independent LLM judge or fresh Claude conversation ran.

Observed operation counts: 5 create_folder, 8 create_file, 16 get_file_metadata, 8 update_file (placement only), 8 batch_update_document, 24 get_document, 1 scoped search; total 70 connector calls. No old-memory edits/deletes. One four-call post-creation retrieval sequence measured 2,168 ms in the orchestration harness; this is NOT end-to-end conversational latency or a general speed claim. No stale-revision race was induced, so accepted guard parameters do not alone prove conflict handling.

The fixture remains available for inspection. Exact IDs, observed links, full read-backs and the operation log are stored in an ignored local private-results file; no account identifiers or private Drive paths are published in this repository. LIVE_028.md still requires Claude's actual recall/answering test. Named title formatting was applied and native content read; no rendered-page visual inspection was performed.
