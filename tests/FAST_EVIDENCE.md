# 0.4.0 evidence

## Verified

178 local tests, including all prior regressions and the FAST verifier/legacy adapter, passed. Coverage includes missing-part invisibility, completion, exact retries, altered duplicate rejection, differing part counts, invalid rows, missing/cyclic/cross-entity parents, missing endpoints, immutable original versions, stale-base conflicts, reconciliation, late unseen branches, literal encoding, topic changes, retirement, legacy History and original IDs, late legacy branches and config validation.

Native disposable workbook:
https://docs.google.com/spreadsheets/d/1mvYazTjqqQaeWTBMED3Jc9xIXj3RtH5uIxCCss9MZPU/edit

Created by importing an artifact-tool workbook with Memory header and a synthetic participant. Actual Codex tools used: import_spreadsheet, get_spreadsheet_metadata, batch_update_spreadsheet (appendCells test transport), get_spreadsheet_range and search_spreadsheet_rows. The fixture holds only synthetic test information.

The live sequence appended only the node part of a two-row operation. Read-back plus the verifier confirmed it was pending, not authoritative. Recovery selected/appended only the original missing edge. Exact read-back verified completion. Two sequential writers using the same base appended different corrections; both heads survived. An identical pair was reappended; the full read-back verified five logical versions, two current preference heads and no duplicate logical fact. A lost-ack simulation found the operation and required no new write. Topic/one-hop retrieval matched the actual saved rows.

These writes use Codex's appendCells **only as the disposable test transport**. The shipped FAST Skill uses Claude append_values. This is not a live test of Claude's append_values, an injected network timeout, physical multi-call atomicity or two authenticated concurrent users. Individual partial rows are rejected; recovery cannot reconstruct lost content after the intended operation is no longer available. No production pointer, memory or original personal Yori was touched.

## Payload and growth

FAST_BENCHMARK.json contains reproducible local measurements. A representative compact fact-plus-edge append request is 423 bytes (453 with default JSON spacing), compared with the user-provided prior compact graph call of 3,857 bytes: about 89% smaller. These are representative requests, not identical encoding of the same records; speaker/source details and IDs differ. Preserved semantics are fact, author/source, edge, stable operation/part and prior references on revision. This is not a latency claim.

Local fixture scales: 10, 1,000 and 10,000 nodes. Cold index construction is O(N); warm map lookups avoid rereading old memory text, but the local harness rebuilds its maps on refresh and is not a performance runtime for Claude. The fixture's person has high degree, so requesting all its edges remains O(N); no silent edge cap. At 10,000 nodes the A:I index is 179,991 cells and needs pagination/tool-cap handling. No sublinear cold-scan claim.

The native workbook was extended to approximately 1,000 nodes. Codex exact topic search returned row 2005, `topic/998`, in 359 ms; one read of A2005:N2006 returned the complete node+edge operation in 467 ms. The search scanned 2,006 rows × 14 columns server-side. It was not an indexed constant-time lookup. These are Codex retrieval measurements, not Claude end-to-end performance. Bulk fixture seeding is excluded from ordinary-save timing; no Claude speed estimate is derived from it.

## Unverified and limitations

Actual Claude response latency, literal parsing/default options, response receipts, direct row search/filter availability, fresh-chat behavior and two authenticated writers require LIVE_FAST.md. The user agreed to run that prompt. No under-10-second success is claimed.

Counts and exact read-back detect partial writes and observed collisions, not all later manual mutations. Model-generated operation tokens are not verified random/unique; complementary partial collisions or indistinguishable operations may be undetectable. Guaranteed ID uniqueness requires an actually exposed trusted ID signal. No exactly-once delivery, CAS, snapshot isolation, immutable ACL or tamper-proof history. Incomplete visibility can exceed the one-read target. Without exact search or retained chat state, a fresh chat needs an index scan. The existing graph remains readable; activation/migration is explicit after validation, and no existing data has been migrated.
