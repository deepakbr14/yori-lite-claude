# 0.4.2 live evidence — fast confirmed saves, 2026-11-15

Provenance: Claude (Opus 5.5) linked to Claude Desktop, real Google Sheets connector, account enupgames@gmail.com, disposable workbooks `1jGoPiZj7DS6_XaRH8kkbcbDI3u3fMQpEen0FnUUckRk` (speed) and `1E3EgYQHeEnL-7kRJrfhIe5jwOrEpfF_FpQojBAmCvcc` (concurrency). No production Cortex or personal Yori touched.

## Method
Save = reply text, then one message with `append_values` and `update_spreadsheet` holding one identity findReplace of the op token (`sheetId` scope, `matchEntireCell`, `matchCase`). `occurrencesChanged` counts every stored cell equal to the op token across the Memory sheet; only column A can hold exactly that value. Zero matches return `findReplace: {}`.

## Connector timings (s, separate calls with clock brackets)
| call | trials |
|---|---|
| append_values, 2 rows | 3.71, 2.71, 2.85 |
| op count (findReplace) | 1.20, 2.15, 1.99 |
| get_values read-back, 2 rows | 1.44, 1.46, 1.79 |
| atomic update_spreadsheet appendCells + count, 1 call (1,424 B vs 424 B) | 5.86, 6.18, 5.74 — rejected |

## Warm end-to-end (s), same session window
| path | reply ready | Sheets | final step | turn total |
|---|---|---|---|---|
| 0.4.2 reply-first, append + count in one message (5 trials) | 1.52 1.88 1.58 1.54 1.74 | 5.76 4.88 5.23 5.15 5.23 | 0.99 1.21 1.05 1.00 1.20 | 8.27 7.98 7.87 7.69 8.17 (median 7.98) |
| 0.4.1 append, then read-back step, then reply (3 trials) | after the turn | — | — | 7.34 7.06 7.46 (median 7.34) |
'Reply ready' is measured after the whole message, including the tool arguments, was generated; streamed text is visible earlier. The final step is a clock call standing in for the final model message.

## Correctness checks (live)
- Count before append: `{}` (0) → recount rule; after append: 2.
- Duplicate retry of the same rows: 4 → check_duplicates.
- Part 1 of 2 only: 1 → pending.
- Stored values unchanged by the identity findReplace (typed `stringValue` confirmed).
- Four simultaneous Claude sessions, 16 append+count saves: every count = 2; all 32 rows present, contiguous per op and exact (`=SUM(A1) 007` literal). First-round receipts again misreported location (three writers told `A41:M42`), which the count ignores.
