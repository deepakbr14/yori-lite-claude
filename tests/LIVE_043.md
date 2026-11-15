# 0.4.3 live evidence — count vs read-back at scale, 2026-11-15

Disposable workbooks (account enupgames@gmail.com), generated server-side and frozen as typed values:
- 1k: `1Ta3s-vXWUBU1sADQ80QXcREku_qnQq-XQaYEqGywYkA` — 1,000 node+edge memories, 2,002 rows
- 10k: `1I_CV-Y2-bQzCJf5K8w5yA2JRz7zWmHewgwXZN2_XBiE` — 10,000 node+edge memories, 20,002 rows
No production Cortex or personal Yori touched.

## Find-and-replace side effects (1k, live)
Hostile cells around token `opHostile123Kq`: the exact token in column A, in text and in subject; the substring `xopHostile123Kqx`; the case variant `OPHOSTILE123KQ`; a trailing-space variant; a formula evaluating to the token; and `007`.
- Typed values before and after the count: identical in every cell (formula intact, `007` still text).
- Sheet-scope count: 3 for a 1-row op (also matched the text and subject cells). An overcount can hide a missing row, so this is unsafe; 0.4.2 used this scope.
- Column-A count: 1 (correct). The formula and the variants were not matched.

## Timings (s, clock brackets around each call)
| | append | column-A count | 20-row window read |
|---|---|---|---|
| 1k | 2.86 2.17 3.33 | 1.83 2.54 2.34 | 2.77 1.93 1.88 |
| 10k | 4.16 2.82 3.08 | 0.94 1.78 1.63 | 1.45 1.49 1.50 |
| earlier small sheet | 3.71 2.71 2.85 | 1.20 2.15 1.99 | 1.44 1.46 1.79 |
Append start hint at the known end instead of A1 (10k): 3.13 3.02 2.93 vs 2.85 2.91 2.80 — no gain.

## Decision
Count is not consistently faster (median ~1.8 s vs ~1.5 s for a read) and verifies presence, not content. Reverted: default verification is a same-message 20-row read after the last row the chat has read, matched by op and exact content. Count is kept as a column-A recovery tool.

## 0.4.3 warm end-to-end on 10k (5 trials, reply first, append + window read in one message)
| reply ready | Sheets | final step | total |
|---|---|---|---|
| 1.50 1.61 1.51 1.35 1.51 | 4.77 4.99 5.28 5.29 5.12 | 0.96 0.97 1.19 1.45 0.99 | 7.24 7.57 7.98 8.09 7.62 (median 7.62) |
Every read showed the exact stored rows. Concurrency: in the earlier 4-writer runs every op landed within 8 rows of the pre-race end, i.e. inside a 20-row window; the window method itself was not re-run under simultaneous writers.
