# FAST Cortex — sheets-log-v1

The complete ordinary FAST save. No Bash, helpers, hashes, manifests or Directory writes; the offline scripts are developer tests. Conversation, Self, selective learning, source fidelity and identity rules live in the main Skill. The original personal Yori is always out of scope.

## Connect once per chat

Preserve My Drive/config_plugins and the fixed plugin config filename/UUID. `storage_format: sheets-log-v1`, `cortex_schema_version: 1` selects one native spreadsheet's **Memory** tab. Existing sheets-graph-v1, Docs and metadata selections keep their readers; never switch automatically. New authorized setup creates Memory with the header below, initializes actual Self, verifies, then writes/verifies the pointer. Account email is optional. Cache for the chat: spreadsheet ID, the Memory tab's numeric `sheetId` (`get_spreadsheet` fields `sheets.properties`), participant entity and relevant current heads.

## Save (warm path)

1. **Reply first.** Write your normal conversational answer, then — in the same message, after the text — issue exactly two calls, in this order:
   - `mcp__Google_Sheets__append_values` with `{"spreadsheetId":ID,"range":"Memory!A1","values":ROWS}`;
   - `mcp__Google_Sheets__update_spreadsheet` with `{"spreadsheetId":ID,"requests":[{"findReplace":{"find":OP,"replacement":OP,"sheetId":SHEET,"matchEntireCell":true,"matchCase":true}}]}`.
   Don't announce the save or narrate it. Don't deliberate over routine rows; use the template below.
2. **Confirm without positions.** Saved when the append says `status: success`, `updatedRows` = rows sent, `updatedCells` = cells sent, and the count reply's `occurrencesChanged` = rows sent. The count is a server-side scan of the whole Memory sheet for cells exactly equal to OP, so it does not depend on where rows landed. Ignore `updatedRange`: simultaneous writers have been told wrong ranges. A count reply of `findReplace: {}` means 0.
3. **After the results,** add nothing to the reply when saved. Otherwise:
   - count 0 with a success receipt → repeat only the count once (the two calls may have run in parallel);
   - count < rows → pending: run the count again; if still short, follow recovery in [fast-details](fast-details.md);
   - count > rows → the token already existed (earlier retry or collision): read the rows carrying OP and compare exactly before anything else;
   - append error or timeout → count first; 0 → re-append the identical rows with the same OP; equal → saved; partial → recovery.
   Never invent a new OP to retry, never lower `total`, never claim an unverified save. Tell the user only when something remains unresolved.

Why it is exact: every nonempty string is sent with one leading apostrophe (Sheets' literal marker, stripped on storage), so no value is parsed as a formula, number, date or boolean — live-verified for 42 hostile values on new and existing workbooks, including rows beyond the original grid. Column formatting is optional; never rely on it. `append_values` applies all rows of one call together; the count confirms all of them exist.

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

Only complete operations are memory. Identical op/part/values count once; same op/part with different values, differing totals or unexpected parts are conflicts, never overwrites. Before current recall, refresh new rows and resolve all heads — see [fast-details](fast-details.md). Model tokens are candidates, not guaranteed-unique IDs; the count exposes reuse of a token already stored, not a collision written later. Never describe this store as tamper-proof or exactly-once.
