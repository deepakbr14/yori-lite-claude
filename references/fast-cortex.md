# FAST Cortex — sheets-log-v1

The complete ordinary FAST save. No Bash, helpers, hashes, manifests or Directory writes; the offline scripts are developer tests. Conversation, Self, selective learning, source fidelity and identity rules live in the main Skill. The original personal Yori is always out of scope.

## Connect once per chat

Preserve My Drive/config_plugins and the fixed plugin config filename/UUID. `storage_format: sheets-log-v1`, `cortex_schema_version: 1` selects one native spreadsheet's **Memory** tab. Existing sheets-graph-v1, Docs and metadata selections keep their readers; never switch automatically. New authorized setup creates Memory with the header below, initializes actual Self, verifies, then writes/verifies the pointer. Account email is optional. Cache for the chat: spreadsheet ID, the Memory tab's numeric `sheetId` (for recovery counts), the last read row `E`, participant entity and relevant current heads.

## Save (warm path)

Keep `E`, the last Memory row this chat has actually read (from the connect read or the last verified save). It is a lower bound; never take it from a receipt's `updatedRange`.

1. **Reply first, without claiming a save.** Write your normal conversational answer. It must not say or imply that anything was remembered or saved. Then, in the same message, issue exactly two calls in this order:
   - `mcp__Google_Sheets__append_values` with `{"spreadsheetId":ID,"range":"Memory!A1","values":ROWS}`;
   - `mcp__Google_Sheets__get_values` with `{"spreadsheetId":ID,"range":"Memory!A{E+1}:N{E+20}"}`.
   If `E` is unknown (first save of a chat), send only the append, then read from the receipt's `tableRange` end + 1.
2. **Verify by content, not position.** Saved when the read contains every part 1..total of OP and each row equals what you sent with the transport apostrophes removed (numbers read back as text, trailing blanks dropped). Other writers' rows may appear in between; that is normal. Set `E` to the last row read.
3. **After the results,** add nothing when saved. Otherwise:
   - OP absent and the window has blank rows → read the same window once more (the calls may have run in parallel);
   - OP absent and all 20 rows are other rows → read the next 20 rows;
   - some parts present → pending: read further; if still short, follow recovery in [fast-details](fast-details.md);
   - same op/part with different content → conflict: stop, keep both, tell the user;
   - append error or timeout → recovery. The column-A count below gives complete coverage of how many rows carry OP.
   Never invent a new OP to retry, never lower `total`, never claim an unverified save. Mention memory only when something remains unresolved.

**Count tool (recovery only):** `update_spreadsheet` with `{"findReplace":{"find":OP,"replacement":OP,"range":{"sheetId":SHEET,"startColumnIndex":0,"endColumnIndex":1},"matchEntireCell":true,"matchCase":true}}`. Its `occurrencesChanged` is the number of rows holding OP anywhere in column A (`{}` means 0). Never use sheet scope: the token can also appear in other columns. It confirms presence, not content.

Why it is exact: every nonempty string is sent with one leading apostrophe (Sheets' literal marker, stripped on storage), so no value is parsed as a formula, number, date or boolean — live-verified for 42 hostile values on new and existing workbooks, including rows beyond the original grid. Column formatting is optional; never rely on it. `append_values` applies all rows of one call together; the read-back confirms their exact content.

## Rows (A:N)

`op | part | total | type | id | parents | kind | subject | object | text | by | basis | source | at`

- `op`: fresh per operation, `op` + 8–40 letters/digits (e.g. `opK7m2Qx9Lw4`); this form survives the count call unchanged. Keep the exact OP and rows until confirmed. Never reuse it for different content. Revision/entity IDs are `op:part`. Readers still accept older tokens (8–128 of letters, digits, `_`, `-`).
- `part`/`total`: JSON integers, slots 1..total (max 100).
- `type`: NODE, EDGE or REVISION. New NODE/EDGE: `id`, `parents` = `""`. REVISION: `id` = existing entity, `parents` = comma-separated exact predecessor revision IDs (all observed heads). Never create a second identity for a correction.
- NODE: `kind` Self/People/Knowledge/Concept; `subject` a readable topic key (`project/langtool/mascot`, `person/<id>/favorite_color`), not an entity ID; `object` `""`; `text` the full small fact with uncertainty.
- EDGE: `kind` the evidenced relation (`about`, `supports`, `contradicts`); `subject`/`object` endpoint entity IDs; `text` the evidence. Unchanged edges need no new row.
- Retirement: `!` before `kind` on a REVISION (`!People`, `!about`), full meaning and reason retained. Retired edges are never active links, even beside a concurrent active head; disclose the disagreement. Reopening is a new revision.
- `by` real contributor or explicit unknown label; `basis` S statement, I inference, D decision, E external, M mixed, U unknown; `source` concise grounded evidence; `at` reliable UTC or omitted. Never invent motive, pronoun, agreement or dates.
- Encoding: in subject, object, text, by, source and at, a value starting `=` `+` `-` `@` `'` `~` gets one extra leading `~`; then every nonempty string gets one leading `'`. Empty interior cells are `""`; omit trailing blank `at`. Readers decode one `~` when followed by one of those characters. Never truncate content.

Template (synthetic):
```json
[["'opK7m2Qx9Lw4",1,2,"'NODE","","","'People","'person/p1/favorite_color","","'Blue.","'p1","'S","'p1: my favorite color is blue"],["'opK7m2Qx9Lw4",2,2,"'EDGE","","","'about","'opK7m2Qx9Lw4:1","'p1:1","'Stated by p1.","'p1","'S","'same"]]
```
The endpoint must already exist. Examples never seed real identities.

Only complete operations are memory. Identical op/part/values count once; same op/part with different values, differing totals or unexpected parts are conflicts, never overwrites. Before current recall, refresh new rows and resolve all heads — see [fast-details](fast-details.md). Model tokens are candidates, not guaranteed-unique IDs; a read showing the same op/part with other content is a conflict. Never describe this store as tamper-proof or exactly-once.
