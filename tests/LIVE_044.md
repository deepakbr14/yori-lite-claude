# 0.4.4 live evidence — one-call saves, single reply, plain voice (2026-11-16)

Provenance: Claude session linked to Claude Desktop, real Google Sheets connector, account enupgames@gmail.com, disposable workbook `1GMP6rDTWqp3Dg_ZxqjHvETQ7YkeSw4kqcss4bW8RgJ8`. The user's own Cortex (`Yori Lite Memory`) was read once, never written. Personal Yori untouched.

## What the user's first real chat showed (0.4.3)
Stored rows were correct (Self, name, favorite color node + edge). Each turn printed the reply twice, once before the Sheets step and again after it, and made two Sheets calls. Replies carried praise and a follow-up question.

## Write primitive (s, clock brackets, 1 row)
| append_values | update_spreadsheet appendCells |
|---|---|
| 2.17 1.59 1.76 | 3.30 3.28 3.26 |
appendCells is slower and needs a 3x larger request; rejected.

## Warm save turn, 0.4.4 path (append only, reply once after the receipt), 5 trials
| model step + append | reply step | turn total |
|---|---|---|
| 3.60 3.73 3.59 3.86 4.24 | 1.06 1.04 1.14 1.17 1.02 | 4.66 4.77 4.73 5.03 5.26 (median 4.77) |
0.4.3 on 2026-11-15: median 7.62. Timings are from this session's own model steps; a real chat adds whatever thinking time the model spends.
Deferred audit: one later 20-row read returned all five operations exactly as sent.

## Fresh sessions following only SKILL.md + fast-cortex.md (3 sessions, 11 turns)
- Sheets calls: first save of a chat = append + read-back; later saves = 1 append; a correction = 1 read + 1 append; no-save turns = 0.
- Two sessions saved at the same moment: both first-save read-backs found their own rows among the other session's rows; all receipts clean; nothing lost.
- `007` and `2026-03-01` inside text stored exactly.
- Replies: "Canberra." / "Sure." / "Okay, no cilantro." / "I'm not sure. I'd want to know what it costs you and how many paying customers started on it…" / "Assuming it's in Rust now: no. Three weeks isn't enough…". No praise, no follow-up questions.
- Row size after the "keep rows small" rule: about 300 bytes for a node + edge (was 413 for the same kind of fact; some earlier saves ran to 4–5 rows and over 1 KB).

## Not established
- How the Desktop app renders text written before a tool call; the Skill now tells the model to write the reply once, wherever its host shows it.
- A failed write with a clean receipt has never been observed; it would go unnoticed until the chat's next Memory read.
- Different Google accounts writing at once; more than four writers.
