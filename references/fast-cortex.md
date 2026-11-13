# FAST Cortex — sheets-log-v1

This is the entire ordinary FAST save procedure. No Bash, helper invocation, hashes, commit manifests, Directory writes or per-cell update_spreadsheet requests. The offline scripts are developer tests, not runtime dependencies. Preserve conversation, Self, selective learning, source fidelity and identity rules in the main Skill. The original personal Yori is always out of scope.

## Connect and read once

Preserve My Drive/config_plugins and the fixed plugin config filename/UUID. `storage_format: sheets-log-v1`, `cortex_schema_version: 1` selects one native spreadsheet's **Memory** tab. Existing sheets-graph-v1, Docs and metadata selections keep their existing readers; never switch them automatically. New authorized setup creates Memory with the header below, initializes actual Self and verifies, then writes/verifies the normal pointer. Guide connection of Drive and Sheets; account email is optional, not an approval gate. No mandatory Project or new authorization.

Use the actual Claude `mcp__Google_Sheets__append_values` interface: known arguments are `spreadsheetId`, `range`, `values`. Inspect current tool definitions, not Codex equivalents. Confirm genuine append and returned location/read-back. Set RAW if exposed; otherwise confirm literal round-trip on disposable rows before active use, with plain-text string columns. Never evaluate memory as formulas. Protect formula-looking literal strings as described below. No direct API workaround. Initial tab creation/header formatting may use setup tools; ordinary saves never do.

## One small operation

1. Reuse this chat's verified config, source, participant and relevant current heads. Each fact is a small node; a preference node is not a new participant. Retrieve established Self before new identity choices. Corrections preserve the entity ID and every observed predecessor; don't pick a timestamp winner.
2. Choose one fresh stable operation token, then short row arrays below. Prefer a host-exposed unique request/message/provider ID usable as a token; no shell preparation. Otherwise use a fresh opaque 128-bit-shaped token as a **candidate**, not a cryptographic or guaranteed-unique ID. Retain the exact token and row arrays in turn context before sending. Never reuse a token for a different operation. See ID limitations below. Roots/revision IDs are derived as `op:part`; no separate row UUIDs. Preserve meaningful sources and reasons, not repetitive prose. Include actual supported edges in the same operation. Limit ordinary operations to a few rows, not bulk profile edits.
3. Call append_values once with `range: "Memory!A1"` and all related rows in `values`. Use append, never write to a guessed next row. Do not assume the call is transactional.
4. Read the returned appended range once, or do one exact operation lookup if a verified complete scoped search is available. Require all distinct parts 1..total, matching counts, exact expected contents/IDs and valid references. An incomplete/mismatched row is pending/corrupt, never saved. A missing receipt/search capability can require extra reads: don't hide these to meet a timing target. No extra read after complete exact verification. No routine narration.

Only a complete operation is visible to recall. No completion marker is needed: every row declares the expected count. Physical order does not establish completeness. Identical op/part and identical full values count once. Same op/part with different values, differing totals or unexpected parts are conflicts, not overwrite candidates. A count is not a checksum. Ignore pending operations as authoritative memory, but report relevant pending/conflicting learning rather than presenting an unset preference.

## Row order (A:N)

`op | part | total | type | id | parents | kind | subject | object | text | by | basis | source | at`

- `op`: stable token, 8–128 letters/digits/underscore/hyphen; never a physical row number. `part`, `total`: positive integer slots/count (max 100). An immutable revision ID is `op:part`.
- `type`: NODE, EDGE or REVISION. For new NODE/EDGE, `id` and `parents` are empty; entity ID is the derived revision ID. REVISION names its existing entity in `id` and comma-separated exact predecessor revision IDs in `parents`. Revision retains its family's fields. Never create a second identity for a correction.
- NODE: `kind` is Self/People/Knowledge/Concept; `subject` is a concise topic key, preferably stable person ID/topic for personal facts; `object` empty. `text` is the meaningful full small fact/reason, uncertainty included.
- EDGE: `kind` is the evidenced relation, `subject`/`object` are stable endpoint entity IDs; `text` explains its evidence. Unchanged edges need no new row. A revised edge is REVISION pointing to the edge entity and its bases.
- Prefix `kind` with `!` on a deliberate retirement revision (for example `!People` or `!about`), retaining full prior meaning and the reason in text. Keep the retired head/history visible; exclude retired edges from active traversal. Reopening is a deliberate new revision, not deletion.
- `by`: actual contributor or explicit unknown-speaker label. `basis`: S explicit statement, I Yori inference, D independent decision, E external evidence, M mixed (attribute claims in text), U unknown. Never convert a guessed motive, pronoun or agreement into a statement.
- `source`: concise original evidence/context or grounded source reference. `at`: reliable recorded UTC time, or blank when unavailable; precise event time remains explicit in source/text, never invented. History is the immutable rows and predecessor links themselves. A revision's text must preserve the current meaning and explain why it changed; do not copy an entire old profile.
- Retain empty interior cells; omit only trailing blank `at`. Strings beginning `=`, `+`, `-`, `@`, apostrophe or `~` are stored with an extra leading `~`; decode exactly one prefix only when the following character is in that set. This keeps such literals inert even if a connector parses entered values. No formula execution. Verify the stored encoded strings before decoding. Never truncate content to meet a payload goal.

Example (synthetic, IDs shortened here; don't reuse):
```json
{"spreadsheetId":"VERIFIED_ID","range":"Memory!A1","values":[["operation_token_1",1,2,"NODE","","","People","person-id/favorite_color","","Blue.","person-id","S","Person: my favorite color is blue."],["operation_token_1",2,2,"EDGE","","","about","operation_token_1:1","person-id","Person stated this preference.","person-id","S","Same statement."]]}
```
The person endpoint must already exist in FAST or the configured legacy reader. Examples never seed real identities. Natural introduction and sole-participant defaults still apply; a shared folder does not authenticate anyone.

## When more context is needed

For an ordinary verified save, stop here. Before current recall, refresh new rows and resolve all heads; a stale row hint or topic hit alone is not authoritative. Use [FAST retrieval, recovery and compatibility](fast-details.md) on fresh-chat retrieval, incomplete writes, concurrency, ID ambiguity or an explicit existing-Cortex switch. Cache the relevant rules instead of rereading every Skill. No complete-cortex text scan on every question.

ID limits apply even on the normal path: candidate model tokens are not guaranteed unique; exact comparison detects observed clashes but not every indistinguishable/complementary collision. Guaranteed uniqueness needs a trusted exposed ID source. Counts detect missing rows, not later well-formed tampering. Never describe this store as tamper-proof or exactly-once.
