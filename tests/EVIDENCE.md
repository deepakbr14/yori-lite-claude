# Evidence for 0.3.1

133 local tests passed. Five real Codex atomic saves and grouped verifications passed; rejected-batch atomicity, immutable originals, conflicting branches and recovery lookup were checked on disposable data. See [measurements and limits](BATCH_031.md). Actual Claude interface, fresh-chat recall, two authenticated writers and end-to-end latency remain pending [live acceptance](LIVE_031.md). No production Cortex or configuration was modified.

# Evidence for 0.3.0

121 local tests passed, including the offline graph utility and prior regression tests. Real Codex Google Sheets fixtures at 10, 1,000 and 10,000 nodes were exercised; see GRAPH_BENCHMARKS.md for exact coverage and timings. New versions preserved both simulated stale-writer contributions. This is not actual Claude or two-authenticated-user acceptance. LIVE_GRAPH.md remains required. Source/config conventions and Docs behavior are retained; no existing user memories or config pointers were changed.

Claude Code package validation passes with the existing warning that the custom metadata manifest field is ignored; the fixed identity also resides in Skills/config. This does not prove claude.ai installation or connector availability. ZIP contents and source parity are checked separately. Standard GitHub marketplace release; live-test limitations remain documented.

## Historical 0.2.8 evidence (unchanged scope)

# Evidence for 0.2.8

The user reports an amber-reason paraphrase added “steady” and precise relative time while visible retrieval showed a related red-request History entry. The earlier production transcript/source sequence was not inspected or repaired here. Source inspection confirmed the need for an explicit current-record-first procedure and saved-versus-new reasoning distinction.

Implemented targeted current Self/People/Knowledge retrieval, relevant addenda/correction handling, business attribution/status fidelity and event-time/timezone grounding. No storage/configuration migration, backend or graph. Independent Self development and automatic selective learning remain active.

Local policy tests cover current-source routing, History-only failure, missing/ambiguous bodies, supported addenda/corrections, original-versus-new reason, unsupported business claims and temporal boundaries. They use structured semantics; they are not a natural-language entailment engine or actual Claude behavior.

Unlike prior source-only releases, this build created and inspected real disposable Google Docs through Codex tools. Exact saved-content/read-back and scoped retrieval assertions passed; see REAL_DOCS_028.md for actual operations and limits. These fixture reads do not establish fresh-conversation Claude recall, paraphrase quality or temporal wording. LIVE_028.md remains required for those behaviors.

Existing and original personal Yori memories were untouched. Only the explicitly disposable test fixture was created. No production config was changed. Marketplace installation and package results are recorded separately.
