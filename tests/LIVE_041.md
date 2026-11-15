# 0.4.1 live evidence — Claude Desktop, 2026-11-14/15

Provenance: Claude (Opus 5.5) session linked to Claude Desktop, real Google Sheets/Drive connectors, connected Google account enupgames@gmail.com. Disposable workbooks only:
- bench `1B1IOIPUfNzsUPQ-nZ6m7CGudCZovCDrB-fCEQ8tn0Yc` (existing since 2026-11-14)
- text-integrity `1x5BZYSWT1KTBewuk6W69BlFChKhFRIzfST07WijKEYk` (new)
- concurrency `1E3EgYQHeEnL-7kRJrfhIe5jwOrEpfF_FpQojBAmCvcc` (new)
No production Cortex, config pointer or personal Yori was read or changed.

## Connector facts
- `append_values(spreadsheetId, range, values)` only; behaves as USER_ENTERED; no RAW, no includeValuesInResponse.
- Receipt: `tableRange` (table before write, absent on an empty tab), `updatedRange`, `updatedRows`, `updatedColumns`, `updatedCells` (cells sent, incl. empty interior), `status`. No values, no request ID.
- `get_values` returns formatted strings and trims trailing blanks. It cannot reveal type coercion that displays identically (`-3`, `TRUE`, `2026-11-14`, `$5`).

## Text integrity (`SHEETS_LITERAL_LIVE.json`)
- Raw strings, rows 1001+ of a new workbook: 24 of 42 values changed type or text; only 14 were visible to `get_values`.
- Plain-text column format: protected numbers/dates within the original grid only; rows created by append beyond row 1000 did not inherit it; formulas and apostrophe stripping were never prevented.
- Apostrophe + `~` codec: 42/42 exact beyond the grid (new workbook) and 42/42 exact inside the formatted grid (existing workbook). Apostrophe alone also stored `=1+1`, `+5`, `-3`, `'quoted`, `(5)`, `#REF!`, `=`, `+`, `-`, `Jan 5`, `3/4` exactly.
- Existing memory rows in the existing workbook were unchanged by every test.

## Incomplete operations and retries (bench workbook, live)
- Part 1 of 2 appended alone: offline audit of the live rows marks the op pending and excludes it; `recover` refuses without full coverage and with coverage plans only part 2.
- Appending only original part 2 completed the op; the edge became an active neighbor.
- Identical part 2 and an identical revision re-appended (lost-ack retry): physical duplicates collapsed to one logical memory; one head.
- Same op/part with different text (separate tab): rejected as an integrity conflict.

## Simultaneous writers (`CONCURRENCY_LIVE.json`)
Four independent Claude subagent sessions, same Google account, synchronized start (spread 0.184 s), five appends each (four node+edge ops and one revision of one shared node).
- 20/20 operations, 36/36 rows present and exact; no loss, overwrite, interleaving inside an op, or literal corruption.
- Four concurrent revisions of the shared node remain four heads.
- 3/20 receipts were wrong: in the first simultaneous round all four writers were told `A3:M4`; only one actually landed there. Rounds 2–5 receipts were correct.
- Not tested: different human Google accounts, more than four writers, network failures mid-call.

## Timing (seconds)
Connector-only, batched calls, includes ~0.17 s clock overhead:
| | append | read-back | total |
|---|---|---|---|
| 2026-11-14, 0.4.0 format | 3.24 / 2.83 / 2.95 | 1.25 / 1.38 / 1.19 | 4.49 / 4.21 / 4.15 |
| 2026-11-15, 0.4.1 format | 4.04 / 3.57 / 3.65 | 1.98 / 2.04 / 2.03 | 6.02 / 5.61 / 5.68 |
The 0.4.1 payload adds ~24 bytes; the day-to-day difference is attributed to service variance, not established as format cost.

Claude end-to-end:
- Warm, in an active session (instructions already loaded; from decision to save through verified read-back, includes model generation and step round trips, excludes the final reply text): 9.89 / 8.38 / 8.61.
- Fresh session (new Claude agent reads the normal route — SKILL.md + fast-cortex.md, 18.9 KB — then learns one fact; scope given, no Drive discovery or recall): first-to-last action 12.66 / 14.17 / 14.59; whole run including agent start 24.3 / 26.7 / 24.3. Three ran in parallel. All three followed the apostrophe rule and verified by op/content.

## Receipt-only decision
Not enabled. Values are protected deterministically, but receipts misreported location under simultaneous writes, so a success receipt is not a proof of where or whether the intended rows landed. Read-back remains the default and matches by op/content, not by position.
