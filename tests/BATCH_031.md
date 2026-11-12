# 0.3.1 optimization evidence — 2026-11-12

## Cause and change

The old protocol separately appended and verified payloads before appending and verifying a commit. Whole-profile updates increased preparation/payload size, History duplicated retained node versions, and Directory maintenance added optional work. The new capability-gated path retains the schema-1 commit manifest but places it last inside the same atomic batch. One grouped read verifies exact immutable IDs, contents and commit. Small preferences become focused nodes with supported relationships to existing participants. Prior versions remain in Nodes; History records attribution, reasons and exact prior revision references. No routine Directory writes. Normal graph instruction routing is main Skill plus graph protocol (two files by design, not measured Claude file activity); setup and edge cases may need more.

## Measured, not estimated

All new measurements below used **Codex's Google Drive plugin**, not Claude's connector. Native disposable workbook: [0.3.1 test](https://docs.google.com/spreadsheets/d/1rvn16kEbPu8kAWTGVnXnzT-Q9LMR9BNMi-dx1ltaTxY/edit). No production memories/configuration were changed.

| Workload | Sheets calls | Write ms | Verify ms | Pipeline ms |
|---|---:|---:|---:|---:|
| New small fact + about edge, trial 1 | 2 | 3069 | 507 | 3576 |
| New small fact + about edge, trial 2 | 2 | 6180 | 705 | 6887 |
| New small fact + about edge, trial 3 | 2 | 3013 | 418 | 3433 |
| Revision A | 2 | 3625 | 445 | 4072 |
| Revision B, same stale base | 2 | 3034 | 458 | 3495 |

New-fact median 3576 ms, range 3433–6887 ms (n=3). Wall-clock pipeline includes small orchestration differences from rounded per-call durations. Optional local Python payload preparation took 0.09–0.25 ms; this excludes host-tool invocation and model reasoning and is not a Claude preparation benchmark.

User-reported Claude baseline: about 33 seconds, nine tools plus reasoning. Earlier 0.3.0 Codex new-node/edge run: six calls, 5770 ms; revisions: five calls, 8532/5554 ms. These are different sessions, small samples and not a controlled Claude speed comparison. The original two-call experiment lacked the exact current protections. We do not claim a 33-to-3-second Claude improvement.

The two-call target covers an already scoped save. Bootstrap, current-head/source reads, connector discovery, UUID/payload preparation, approvals and exceptional recovery add calls/time. Approval duration, model overhead, first-chat timing and fresh-chat latency were not observable here. Skills cannot bypass connector approval dialogs. No slowdown has been attributed to authorization without timing evidence.

## Actual operations and assertions

- Copied a clean synthetic ten-node/ten-edge workbook using Drive; read sheet IDs/grid bounds and baseline cells.
- `batch_update_spreadsheet` with multiple genuine `appendCells` subrequests, including commit last. Invalid final sheet-ID subrequest returned HTTP 400; grouped `get_spreadsheet_cells` showed no earlier appends. This verifies atomic rejection for the Codex interface tested, not Claude.
- Five successful atomic writes, each followed by one `get_spreadsheet_cells` across all touched tab windows. Exact planned contents/IDs matched. Returned grid bounds constrain reads; observed prior row positions are hints only. A missing expected ID requires extra lookup, never false verification.
- Full grouped audit matched the independently expected workbook: 15 physical Node versions, 13 logical nodes, 13 edges, 50 History rows. All original rows and Directory were unchanged. The two stale-base revisions remained competing heads.
- Warm one-hop and recovery lookup used one grouped read (1171 ms) across verified row hints, endpoint nodes, revisions and relevant History. IDs/endpoints matched. Local recovery classified the original operation as already committed and issued no write. This simulates a lost acknowledgment using actual saved data; no transport timeout was injected.
- 133 local tests pass, including exact retry IDs, identical duplicate deduplication, mismatching duplicates, incomplete-window recovery, partial initialization, competing heads, prior version retention and schema compatibility. Local tests are not Claude conversational acceptance.

## Limits

Claude tool interfaces remain unverified from this environment. The Skill must inspect them and select atomic mode only when supported; otherwise preserve staged writes. An atomic append is not compare-and-swap against an earlier read. Simultaneous independent users were not tested; the stale-writer simulation was sequential under one account. Fresh-chat recall, autonomous edge selection, natural granularity and first/subsequent chat latency require [the live Claude procedure](LIVE_031.md). Broad scans at scale, uncertain results or missing receipts can exceed the two-call target. Logical retry deduplication is not exactly-once physical delivery. The optional preparation helper has no network access; it does not itself supply a connector or validate unseen external references.
