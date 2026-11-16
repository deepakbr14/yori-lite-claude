# 0.4.4 — One Sheets call per save, one reply, plain voice

- Ordinary save is a single `append_values`. The write is confirmed from the receipt (success, row count, cell count, Memory column A; row numbers ignored). The exact-content read-back now runs in the same turn only for a chat's first save or an unclean receipt; every other save is audited by content at the chat's next Memory read.
- The reply is written exactly once: before the call where the host shows such text, otherwise once after the receipt. No repeated or reworded reply after the save.
- New Voice section: plain, short, honest; no praise or pleasantries, no questions asked to keep the conversation going, says "I don't know" and "I disagree".
- `receipt_ok()`, `after_append()`, `audit_saved()` with regression tests; evidence `tests/LIVE_044.md`.
- Residual: a write that fails despite a clean receipt (never observed in 150+ live appends) would not be noticed in the same turn, and is lost if the chat ends before its next read.

# 0.4.3 — Read-back restored as default; count fixed to column A (development branch)

- Default verification is again a content read-back, now issued in the same message as the append over 20 rows after the last row the chat has read, matched by op and exact content (never the receipt position). The reply still comes first and must not claim a save.
- The 0.4.2 count is demoted to a recovery tool and scoped to column A: live, sheet scope overcounted (3 for 1) when the token also appeared in other columns. Find-and-replace changed no unrelated values.
- At 1k/10k memories the count was not faster than a read (~1.8 s vs ~1.5 s); append ~2.9 s at any size; an append start hint did not help.
- 10k-memory warm save: reply ready median 1.51 s, verified total median 7.62 s.
- `locate()`, `window_range()`, `expected_read()` with regression tests; evidence `tests/LIVE_043.md`.

# 0.4.2 — Reply-first saves with position-independent confirmation (development branch)

- Normal save: the conversational reply is written first; the same message then sends `append_values` plus a whole-sheet op count (`update_spreadsheet` identity findReplace). The count replaces the positional read-back, ignores the unreliable `updatedRange`, gives complete coverage for recovery and exposes reuse of an existing token.
- New op tokens: `op` + 8–40 letters/digits (safe to re-enter during the count). Older tokens remain readable.
- `fast-cortex.md` rewritten as a short recipe with a template (8,830 → 5,867 bytes). Readable topic keys in `subject`.
- Live: reply ready median 1.58 s (was after the whole ~7–10 s turn); full verified turn median 7.98 s vs 7.34 s for 0.4.1 in the same window. Sheets calls still 2. An atomic one-call variant was slower (5.7–6.2 s) and rejected.
- `confirm()`, `count_request()`, `count_from_reply()`, `new_op_ok()` with regression tests; evidence in `tests/LIVE_042.md`, `tests/CONCURRENCY_042.json`.

# 0.4.1 — FAST correctness fixes (development branch)

- Retired edges never appear in active traversal, even beside a concurrent active head; `contested()` and `history()` expose the disagreement and the retired history explicitly.
- The `~` literal codec is decoded uniformly on subject, object, text, by, source and at (previously only text, by and source).
- Exact Google Sheets values: the Claude `append_values` connector has no RAW option and parses cells like typed input. Every nonempty string cell is now sent with one leading apostrophe (Sheets' literal marker). Live-verified for 42 hostile values (formulas, leading zeros, scientific-looking strings, dates, times, currency, percents, booleans, error literals, apostrophes, Unicode, newlines, padding) on a new workbook beyond its original 1,000-row grid and on an existing workbook. Plain-text column formatting alone failed beyond the grid and is no longer relied on.
- Readers accept `get_values` string part/total and trimmed trailing cells.
- Verification matches rows by op/part/content, not receipt position: in a live test with four simultaneous Claude sessions, 3 of 20 receipts reported a wrong `updatedRange` although no row was lost or overwritten. Receipt-only saves remain disabled; read-back stays the default.
- New regression tests and live evidence: `tests/SHEETS_LITERAL_LIVE.json`, `tests/CONCURRENCY_LIVE.json`, `tests/LIVE_041.md`.
- Storage format, config, existing rows and revisions are unchanged; rollback to 0.4.0 needs no data change, but 0.4.0 writers must not be used after 0.4.1 on the same Cortex because they send unprotected strings.

# 0.4.0 — FAST single-tab Cortex

- Adds compact NODE/EDGE/REVISION rows through Claude append_values; one related-row append plus verification when supported.
- Removes normal FAST Bash preparation, per-cell JSON, hashes, duplicate History and commit markers. Part/total completeness and exact stable-ID retries handle partial operations.
- Preserves conflicting revisions, attribution and original meaning; adds in-chat ID/topic/relationship maps and tail refresh.
- Reads existing five-tab graphs unchanged, including old History and revisions. Optional dual reader preserves original IDs; activation is explicit after validation, never automatic migration.
- Disposable native workbook correctness tests and local scale tests passed. Actual Claude benchmarks and two authenticated writers remain pending; limits on model-generated IDs, manual edits, cold scans and exactly-once delivery are explicit.

# 0.3.2 — Compact save requests

- Remove every per-cell formatting block, omit trailing empty cells, use positional empty cells, and combine History contribution/commit in one append request.
- Save a small node plus supported edge; History points to its immutable revision instead of copying its text. Remove descriptive bookkeeping from commit markers, preserving required schema-1 checks.
- Package a fixed small-intent preparation helper with durable local retry plans; no newly generated Bash scripts, hand-built transactions or extra hash tools.
- Replace the long ordinary save procedure with five steps; recovery details load only on exceptions. Keep one necessary grouped verification.
- Preserve config, schema, prior versions, attribution, branches, Self and original personal Yori. No migration.
- Comparable encoder input: 10,147 → 3,297 compact JSON bytes (67.5% smaller). This is not the user's exact 4,037-byte request and is not a Claude timing benchmark. Claude acceptance remains pending tests/LIVE_032.md.

# 0.3.1 — Smaller memories, fewer sequential calls

- Save focused preference nodes anchored to existing participants; preserve profiles and stable identities.
- Capability-gated atomic append of Nodes, Edges, History and the existing commit marker, followed by grouped verification; safe staged fallback remains.
- Reference immutable prior versions instead of redundant snapshots; preserve attribution, branches and uncertain-response reconciliation.
- No routine Directory writes. Normal graph instructions route through the main Skill and graph protocol; additional references load when needed.
- Same schema and bootstrap, no migration or production memory edits. Measured Codex results and pending Claude acceptance are separated in tests/BATCH_031.md.

# 0.3.0 — Sheets graph Cortex

Standard GitHub marketplace update. Adds full node/edge version rows, append-only logical commits, Directory hints with ID checks, conflict branches, bounded traversal, staged Docs migration and rollback. Keeps existing configuration/bootstrap and all Docs behavior unless graph storage is explicitly selected. Actual Claude capabilities, fresh-chat recall, two-user conflicts and scale acceptance remain pending.

# Changelog

## 0.2.8

- Route established-memory recall to the relevant current Self/People/Knowledge record before History; require targeted lookup for History-only hits.
- Separate saved meaning from present interpretations and new reasoning without forcing verbatim replies or constraining independent Self development.
- Preserve business speaker/motive/decision/commitment status and qualify temporal wording using actual event/timezone evidence.
- Keep storage, migration, participant recognition, autonomous learning and History safeguards unchanged. Existing experimental memories are not repaired.


## 0.2.7

- Recognize a sole known participant conversationally without repeated identity questions or sharing disclaimers; preserve the inferred basis.
- Persist evidenced account-to-existing-People associations when actual identity tools provide usable signals, without conflating Google/Claude accounts or human identity.
- Resolve shared-Cortex ambiguity only when needed; do not disclose personal history while unsure who is speaking. Preserve unknown-speaker learning and corrections.
- No storage/config migration or new authentication backend. Actual Claude identity interface remains pending live verification; Codex profile signal evidence is labelled separately.


## 0.2.6

- Move primary memory to readable Google Docs bodies; onboarding guides connection of both Google Drive and Google Docs.
- Preserve automatic selective learning, independent Self continuity, neutral attributes and claim-level provenance.
- Keep History append-only; snapshot before guarded edits, with verified non-destructive addenda when revision controls are absent.
- Add resumable metadata-to-body migration, source retention, stable logical identity and per-record verified authority. Optional config storage_format distinguishes legacy/mixed/docs-v2.
- Preserve config filename/UUID and four Cortex folders. No automatic old-data cleanup, graph, server or custom MCP.
- User-reported Claude Docs create/read/edit/read-back passed; full lifecycle/migration/concurrency/latency remains live validation.

## 0.2.5

- Require fresh-chat Self retrieval and evidence-based preference continuity; distinguish unknown recall from a new or deliberately revised preference.
- Explicitly learn Yori's own considered choices and preserve reasons/history without duplicating unchanged preferences.
- Introduce people naturally after setup when their names are unknown, with existing-record reuse and shared-Cortex identity safeguards.
- Reuse scoped Self/People evidence across Skills; no storage/schema migration. Incident root cause remains unconfirmed pending actual metadata/Claude traces.


## 0.2.4

- Fix the account-identification regression: “make one” authorizes setup through the existing Drive connection even when the account email is unknown.
- Remove unnecessary account questions, unsupported capability claims and repeated internal progress narration; retain actual authentication/scope checks and verified completion.
- Storage, learning, correction history and concurrency protocol remain unchanged. Actual Claude connector acceptance test remains pending; no static test is represented as end-to-end proof.


## 0.2.3

- Carry setup authorization through folder creation, initialization, pointer configuration and verification without redundant approvals.
- Ask one necessary account question and stop; reuse prior answers, explain sharing once as information, and keep routine operations and successful retries quiet.
- Apply initiative, independent judgment and concise, relevant conversation across all five Skills; examples are illustrative rather than scripts.
- Preserve storage protocol, configuration, identity, memory templates and safe documentation maintenance unchanged. Live Claude behavior remains a required check.


## 0.2.2

- Promote yori-lite as the entry point for conversation and explicit setup; helpers stay available internally, with namespace limitations documented.
- Welcome normal missing-config setup, verify the connected account before resource creation, and keep implementation/URLs out of routine dialogue.
- Rewrite config_plugins README as a readable, vendor-neutral developer convention with two unrelated plugin examples.
- Stop creating Cortex READMEs; guard narrowly verified retirement of unchanged setup-generated guides, preserving user files and memory.
- Consolidate the repeated operating contract and clarify the new-topic call path without dropping contribution/topic records or verification.
- Apply a purposeful-question check across every skill; preserve real curiosity and reasoned opinions.

## 0.2.1

- Apply colleague-like dialogue across all skills: no routine engagement questions or three-choice prompts; preserve independent judgment and warranted curiosity.
- Finish setup naturally without soliciting another topic.
- Create human-readable README body files; additive repair preserves existing config, Cortex, readable guides and metadata-only originals.
- Reuse verified context/searches within a turn and schedule independent operations where supported, keeping guard/history/read-back dependencies intact.
- Document the reported 35-second Aurora latency without claiming an unmeasured speedup.

## 0.2.0

- Store memories in Google Drive descriptions with empty file contents; target roughly 4,000 characters.
- Revise memories with actual etag guards and bounded reconciliation retries.
- Preserve each meaningful contribution and prior version in metadata History records.
- Make setup, recall, learning and errors conversational; one question at a time.
- Keep developing Self in the Cortex, with autonomous learning and evidence-preserving reorganization.
- Preserve fixed config identity, add metadata config with legacy read compatibility, and defer Cortex switching.
- Keep public GitHub marketplace distribution; no personal Yori integration or new infrastructure.

## 0.1.0

Initial independent Skills plugin and GitHub marketplace. Prior tests and design are retained in Git history; they are not evidence for the 0.2 live behavior.
