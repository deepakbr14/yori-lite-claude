# Claude FAST test — 0.4.0

Install 0.4.0, start a fresh Claude chat, and paste the following. This is pending live Claude acceptance, not an already-passed benchmark.

> Test Yori Lite FAST in a NEW disposable workbook only. Do not switch my real config, migrate memories, or access original personal Yori. Use sheets-log-v1: one Memory tab, NODE/EDGE/REVISION arrays. Inspect the actual append_values and read schemas and record their exact names. Check literal values round-trip; do not assume one append is transactional.
>
> Create synthetic participant Alex. Then learn “my favorite color is blue” as a small node plus an about edge in one append_values call. No Bash, generated scripts, hashes, commit manifest, profile rewrite or per-cell JSON. Use the returned range for one exact verification read where available. Repeat three small saves; record actual argument bytes, connector calls, write time, read time and total response time where observable. Count bootstrap, ID discovery and model time separately; mark unknowns unknown. Targets are under 10 seconds, ideally 3–5, not asserted outcomes.
>
> Correct blue to green, keeping the same entity ID, original version, author, reason and source. Inject a two-row operation with only its first row: it must stay pending. Resume by appending only the second original row, then verify. Simulate a lost response after a complete write: find the original operation and do not create a new one. Test an identical whole-call retry; count it once logically. Test altered content under the same op/part: report conflict, never choose a winner. Keep deliberately corrupt tests in a separate disposable workbook so they do not invalidate the normal test scope.
>
> Have two sessions read the same preference revision and append different corrections. Both must remain heads with distinct attribution until explicit reconciliation. If only one user is available, label this a stale-writer simulation, not a two-user test. Try a malformed/truncated row separately: block its use rather than invent missing content. Identify any limit on recovery, ID uniqueness or literal parsing.
>
> Restart the conversation using only this disposable workbook ID and recall the current preference and related person; expose conflicting heads. Check source fidelity and Self continuity with one synthetic Self preference and its original reason. Do not copy prior answers into the fresh chat. Test an ordinary question after warm-up: reuse context and refresh the append tail instead of rescanning all memory text.

## Optional scale check (read-only)

A prepared native disposable fixture contains about 1,000 nodes plus their relationships:
https://docs.google.com/spreadsheets/d/1mvYazTjqqQaeWTBMED3Jc9xIXj3RtH5uIxCCss9MZPU/edit

Ask for `topic/998`, verify both parts of its operation and its about edge to `fixture0:1`. Measure a fresh-chat lookup and then three warm lookups; report scan bounds/cells and tool calls. Do not assume Claude exposes Codex's search_spreadsheet_rows. If only ranges exist, measure the one-time A:I index scan and subsequent tail/targeted reads. This fixture also retains two conflicting synthetic color revisions; don't “repair” them for testing.

## Report

Return actual payload bytes and total response time, call counts, first/warm differences, correctness checks and unresolved limitations. If the UI cannot expose timing, measure externally; do not infer latency from bytes. Do not activate FAST on the real Cortex until these tests pass and I explicitly request the switch.
