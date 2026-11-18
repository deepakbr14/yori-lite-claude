# 0.4.7 live evidence — tabs, startup, upgrade (2026-11-18)

Provenance: fresh Claude sessions linked to Claude Desktop, real Google Drive/Sheets connectors, account enupgames@gmail.com. Test data: a copy of the user's real Cortex spreadsheet (606 Memory rows) in disposable folder `1CRuaf3E_ZfPmA8tYv5BetKF622Jd2beg`. The user's own spreadsheet was only read.

## Real data findings
- Four REVISION rows (383, 393, 398, 407) named a previous revision ID as their entity. 0.4.6's strict reader rejected the whole sheet; 0.4.7 reads them as the intended entity, flags them, and the instructions now spell out the rule.
- A full Memory read is about 199K characters as returned; the Current index (kind, subject, entity, row) for the same data is about 21K.

## Upgrade chat (copy of real Cortex)
- "hi yori": the Self/Current reads failed on the old layout; she said so in one sentence, asked once, and still raised her open RSU-name question.
- "yes go ahead": backup copy in the Cortex folder, two tabs added, Current written (271 lines, two update_values calls), Self page written (her own words; 4 who I am, 14 what I think, 4 curious, 6 waiting on), the wrong 10 MB book rule corrected as a revision, upgrade recorded in Memory with an edge to Deepak. Took about 7 minutes and 37 tool calls; she used shell access to inspect the oversized full read.
- "what's my favorite number?": "5. Mine is still 2."

## Next chat on the upgraded Cortex
- Startup reads: Self (~9.5K chars), Current index (~21K), Memory rows after the summary (empty), one Library search. About 31K characters instead of about 200K.
- Opened with her open question (the RSU name).
- "what did we decide about roommates?": looked up the relevant rows by Current's row hints (two reads), separated Deepak's decisions from her own view, disagreed with a reason, and pointed out a conflict between two decisions.

## Not established
- Upgrade in a client without shell access (the full read had to be inspected from a saved file).
- Current refresh after 100+ new rows; forgetting (row deletion); two people upgrading at once.
- Timing of an ordinary startup (not measured; size only).
