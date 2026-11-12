# Graph benchmark evidence — 2026-11-11

Live tests used **Codex Google Drive tools, not Claude**. Model overhead and Claude response latency are unknown. Fixtures are synthetic, short and low-degree. No production memory, config pointer or original personal Yori was changed. No migration was activated.

## Measured native Sheets reads

Three trials per primitive; median elapsed connector seconds, one call each. Direct read returns a full node, while ID search returns a location needing a subsequent full read. These are not equivalent complete recall workloads. Category scans D:F; incident-edge search scans D:E, within Codex's exposed 50,000-cell search cap at all sizes. Exact-match filtering and complete pagination remain necessary.

| Nodes / edges | Direct full row | ID location search | Category search | Incident-edge location search |
|---|---:|---:|---:|---:|
| 10 / 10 | 0.320 | 0.310 | 0.379 | 0.308 |
| 1,000 / 1,000 | 0.333 | 0.404 | 0.445 | 0.383 |
| 10,000 / 10,000 | 0.745 | 0.808 | 0.849 | 0.821 |

Direct access was not consistently faster, and it cannot replace head/commit checks. A separate Launch keyword search returned four matches without truncation at each size (one trial).

## Traversal with full records and supporting History

Single trials. The harness searched both edge endpoints, fetched complete edges, found/read neighbor nodes, and retrieved their contributions and commit manifests. Independent reads ran in batches of up to four. Actual returned subgraphs passed offline verification of commit hashes, references and revision heads. Hash computation, bootstrap, participant recognition, reasoning and response generation are excluded from connector wall time.

| Size | One hop: calls / seconds | Two hops: calls / seconds |
|---|---:|---:|
| 10 | 15 / 4.526 | 26 / 4.607 |
| 1,000 | 15 / 3.710 | 29 / 5.856 |
| 10,000 | 15 / 7.966 | 29 / 14.817 |

The root was the launch decision, retaining its explicit agreement and earlier distinct positions. One-hop results contained four nodes and three edges at every size. Two-hop results contained six nodes/six edges at size 10 and seven nodes/seven edges at larger sizes because the synthetic scale chain adds a boundary neighbor. These are not identical-subgraph scaling ratios.

Self with reading-light context and History: ten calls, 1.924 seconds at size 10 and 5.414 seconds at size 10,000; two nodes/two edges. Original amber reasoning was verified. These clean fixtures have one current head; no fresh Claude conversation or paraphrase test ran.

## Native writes, stale writers and retries

Tests used a separate copy so the starter remains clean. Payload records were appended/read back before appending/verifying the commit. No existing memory row was replaced.

- New attributed node and supported edge: **6 calls, 5.770 seconds** summed connector time.
- First revision, with full prior-state snapshot and contribution: **5 calls, 8.532 seconds**.
- A second revision based on the SAME old baseline: **5 calls, 5.554 seconds**.
- Native readback passed the audit: 11 logical nodes, 11 edges, and one Self entity with BOTH current branches. All original Nodes, Edges and History rows remained exactly equal in decoded values; original meaning and both new reasons survived.
- Retry lookup found the existing operation's contribution and commit, reused verified payloads and performed no second append. Physical duplicate injection and conflicting row-ID payloads were tested locally, not live.

These were logical stale writers through ONE connected account, sequentially. They do not pass two-authenticated-user or simultaneous-append acceptance. UUIDs/hashes came from trusted local Python; Claude generator availability is unverified. Write timings start with prepared payloads and a previously verified baseline/scope. Directory hints are optional and were not added; no unverified current-state assumption depends on them.

## Scale and fidelity coverage

Real workbooks were imported at 10, 1,000 and 10,000 nodes with equal edge counts and 40, 4,000 and 40,000 History rows. All five tabs of the small workbook matched every expected field, timestamp and manifest. Local previews were inspected and native formatting metadata read; no native-browser visual check ran.

All 10,000 native node IDs matched source order exactly and were unique. Full larger-workbook bodies were sampled through direct reads and retrieved subgraphs; no full all-cell audit of both larger workbooks ran. This does not establish semantic accuracy for every large-workbook cell.

GRAPH_SCALE_LOCAL.json records local Python correctness/scale timings at the same sizes. It exercises full audit, ID lookup, one/two-hop traversal, node/edge creation and revision preservation. Google calls are zero. Whole-book materialization is an offline harness, not the recommended runtime read strategy. Results do not predict Claude latency.

## Comparison with earlier Docs measurements

Prior Codex study: Self 0.394 seconds; person 0.488; decision plus three History Docs 0.394 with four parallel calls; new fact/contribution 28.536 across 14 calls; preserved revision 24.106 across 17 calls. Those were different payloads in an eight-record corpus, with file creation/placement checks and a Docs revision guard. Fast parallel Docs reads cannot be compared directly with a graph traversal of many more sources. Graph results suggest fewer file-lifecycle calls, not a proven Claude response improvement. The previous simple two-call Sheets write did not implement this graph commit protocol.

## Actual interfaces and limits

Exercised Codex tools: create_folder, import_spreadsheet, copy_file, get_spreadsheet_metadata, get_spreadsheet_range, get_spreadsheet_cells, search_spreadsheet_rows, batch_update_spreadsheet using appendCells. No conditional Sheets write precondition was exposed. Actual Claude tool definitions are inaccessible from this session; LIVE_GRAPH.md gives the required exact probe. Public API capabilities alone are not evidence of Claude support.

Skills do not enforce database transactions or immutability. Human edits can corrupt records; hashes detect inconsistency but do not authenticate an author. Workbook permissions apply to all tabs. Missing safe append, trusted IDs, complete reads or recovery can block dependent writes. Wide/high-degree queries and commit discovery can be slow. Directory never proves completeness. Over-limit cells/manifests must be reported; multipart memories are not implemented. Legacy baseline/addendum identities need explicit migration mapping. Rollback must preserve graph-only learning before claiming continuity.

Actual Claude learning/recall, two independent users, ambiguous-acknowledgement recovery and live migration/rollback remain NOT VALIDATED. No production readiness claim.

## Disposable native files

- [Clean 10-node starter](https://docs.google.com/spreadsheets/d/10DidvDqBe3mQ2sVreDqtGbSR2HVBTu_POBCzU3hdFCc/edit)
- [1,000-node benchmark](https://docs.google.com/spreadsheets/d/1EKbcAq29rBbYT1Q76YC05MksGH8vLy4tzEpr7Ykf3II/edit)
- [10,000-node benchmark](https://docs.google.com/spreadsheets/d/1ntyQM8QKRjW4_KCp2NP-Is0-GotnaYT44iuNr73Bnh4/edit)
- [Write/conflict copy](https://docs.google.com/spreadsheets/d/100tZdpEAglkMD-gz0QWhlLry6TpOdWcEU0DPD5FlMGM/edit)

Private local raw tool receipts are excluded from the plugin ZIP. The clean JSON fixture, schema, offline utility, local scale results and Claude test script are included.
