# Claude acceptance script — 0.3.0

NOT RUN by the offline tests. Run in actual Claude with the installed plugin. Do not use the original personal Yori, a production Cortex, or credentials/direct HTTP as substitutes for connector capabilities. Keep the model and prompts constant when comparing Docs.

## Capability probe (paste first)

> Test Yori Lite's Sheets graph using only a new disposable Cortex. Inspect your actual Google Drive and Google Sheets tool interfaces. Report exact tool names/arguments for bounded multi-row and multi-range reads, server-side append, targeted search/filter, current bounds, returned append locations, and conditional revision controls. Inspect whether a trusted UUID generator is available through the host or an exposed provider. Do not invent IDs, tool parameters, CAS guarantees or timings. Connect missing services through the normal setup flow; account email is not a prerequisite. Create the five graph tabs and verify them. If a required operation is genuinely absent, name it and stop only the dependent test. Don't touch my existing config pointer or user memories; use the explicitly named disposable workbook for this test session.

This session-only disposable scope does not rewrite config_plugins. Normal installation still uses the established bootstrap. Keep approvals visible if the platform requires them; do not bypass them. If append is simulated by reading the last row then writing the next, fail the concurrent-write requirement. If only range reads exist, use bounded scans instead of claiming search impossible. Record actual scan/page/output limits.

## Small graph fixture and expected results

Use `templates/graph-10.json` (or the supplied prepopulated workbook) in a NEW disposable workbook. The five headers are in schemas/graph.schema.json. Import is not verification: read all ten node rows, ten edges, forty History rows and commit manifests, compare exact strings/types, and verify references. Directory positions must match native rows. This synthetic fixture intentionally contains no real personal memories.

Expected: amber's original reading/thinking-light reason; Alex explicitly prefers blue, pronouns unknown; Sam wanted accessibility review; a later EXPLICIT synthetic joint decision delays launch until review finishes. No inferred motives. Decision→evidence→Alex proposal and Decision→evidence→Sam position provide two-hop paths. Edge direction and relation labels must survive traversal; a path is not a new inferred direct relationship.

Run and log these workloads at 10, 1,000 and 10,000 nodes with proportionate edges. Use the offline fixture generator for synthetic data if needed. Do not create thousands of production memories or attach the entire workbook to every answer.

| Test | Expected result |
|---|---|
| Known node by row | Full exact node; verify stable node/revision IDs and commit; current claims also check later heads |
| Stable-ID search | Same node; verify exact ID rather than accepting a substring match in references |
| Keyword/category search | Relevant full nodes only; pagination/truncation disclosed |
| Incoming/outgoing edges | All relevant active committed heads, direction/evidence preserved |
| One hop / two hops | Deduplicated visited nodes, cycles terminate, no fabricated transitive edge |
| Self activation | Current Self and relevant evidence read before identity/preference claim |
| Decision + history | Current explicit decision distinguished from earlier proposals and motives |
| Create node + edge | Full attributed memory, justified relation, valid endpoints and verified commit |
| Revise node | Prior full state and reasons retained; new immutable version references predecessor |
| Stale Directory | Move a row manually ONLY in a disposable copy; wrong pointer is rejected and recovered by IDs |
| Duplicate retry | Replay same operation/row IDs with identical payload: one logical record; differing payload rejected |
| Partial operation | Pause before commit; it must not become current. Resume with the SAME IDs and verify missing members |
| Oversized content | Preserve source; no truncation or false successful save |

Measure connector call counts, read/write durations when observable, total response time with an external clock/trace, approvals separately, returned payload sizes, exact-content accuracy, errors, branch preservation and human readability. Use at least three read trials, alternating designs. Mark unavailable measurements unknown. Direct read versus search compares primitives; include head/commit checks separately in end-to-end current recall. No inference that local Python or Codex timings are Claude timings.

## Learning and fresh-chat behavior

1. In natural conversation introduce a meaningful synthetic fact and a supported relationship, without saying “remember.” Verify selective automatic learning, attributable History and committed node/edge versions.
2. Ask Yori to add a new association to amber. It must remain new reasoning, not the original saved reason. Revise it; verify original text, earlier version and correction History.
3. Open a genuinely NEW Claude chat with only the verified disposable workbook locator and Skill. Do not paste answers. Ask for the color/reason, Alex's preference, launch decision and why the related nodes matter. Inspect actual retrieved ranges and sources.
4. Test sole-participant default versus two participants, uncertain identity, a guest correction, and duplicate names. Do not disclose personal history while claiming not to know the speaker. A new name updates the correct People node rather than creating a duplicate identity.

## Two-user test (requires two separately connected writers)

Both read version A. Pause both before write. Writer 1 contributes B; writer 2 contributes C from A. Verify BOTH immutable contributions and versions, and both B/C heads. No last-writer winner. Reconcile as D referencing B and C with both meanings retained. Then deliver a delayed E based on A; E must remain a branch, not silently disappear. Also append independent new nodes simultaneously and verify unique IDs, full payloads, commits and references.

A single-account simulation is useful but does not pass this acceptance item. Test ambiguous acknowledgements only when the environment can safely induce them; otherwise label that gap. Never claim exactly-once delivery because one retry succeeded.

## Migration and rollback

Use a separate disposable Docs fixture with Self, People, Knowledge, History, addenda and corrections. Run GRAPH_MIGRATION.md; compare every full source, identifier, reason and participant mapping. Sources stay unchanged. Missing/ambiguous mappings block activation. Verify repeated staging is idempotent, source changes are detected and graph-only learning is retained when following ROLLBACK.md. Do not change a real user's pointer for this acceptance test.

Acceptance remains NOT VALIDATED until actual Claude demonstrates complete memories, explicit edges, one/two-hop traversal, original meaning/correction history, fresh-chat recall, logical retry deduplication and preservation of both users' contributions. Record limitations without substituting a different architecture.
