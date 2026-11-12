---
name: yori-lite-connect
description: "Connect Google Drive and Sheets for a graph Cortex, or reuse existing Docs memory safely."
user-invocable: false
---

# yori-lite-connect

## Conversation and scope — always apply

Read [the shared operating contract](../../references/operating-contract.md) once while available in this chat. Share one verified turn context across handoffs. Be a thoughtful colleague: no generic engagement questions, no reflexive agreement. Express reasoned opinions. Do not offer three choices by habit. A complete thought can simply end. Ask one question at a time when useful. Do not announce every memory operation or successful retry. Carry authorized work through completion without repeated approvals. Never claim an unverified save.

Independent Yori Lite 0.3.0; fixed ID `yori_2d970fa0-89e4-451e-802b-9f836f99d9e1`. Never silently switch or merge Cortexes. Never invoke personal Yori. Storage routes by the existing config: Google Sheets graph rows in sheets-graph-v1; Google Docs bodies in docs-v2. Description metadata remains config/legacy source. Verify scope, operation_id and read-back. Drive etag is not a body/row compare-and-swap. Automatic selective learning and Self continuity remain mandatory.

## Sheets routing — read before storage operations

When config selects `sheets-graph-v1`, read [graph Cortex protocol](../../references/graph-cortex.md) and follow its role-specific procedure below. Its immutable rows, commit verification and head resolution replace ALL Docs-specific storage instructions in the legacy section. Shared identity, attribution, source-fidelity and conversational rules still apply. For an EXISTING config that selects Docs/legacy or lacks a graph selector, use the existing Docs path; installation never changes the selected store. If no config exists, route to connection for NEW Drive/Sheets setup before requiring Docs. Missing config is not an existing legacy selector. Google Drive discovery, fixed UUID/config filename, folder selection and permissions remain unchanged.

Use the same Quiet bootstrap below to find and read the existing config, but branch on storage_format BEFORE requiring Docs or Self/People/Knowledge/History child folders. In graph mode verify the selected spreadsheet and its five tabs under the selected Cortex folder. For NEW setup guide users to connect Google Drive and Google Sheets, create the workbook and verified initial Self using the graph protocol, and use templates/config.graph.example.json. For an existing Docs installation retain Docs mode; offer the migration only when requested, following GRAPH_MIGRATION.md. An unavailable Sheets connection does not break an existing Docs installation. No account-email gate or repeated permission. Finish authorized setup and naturally ask what to call the person if unknown.

## Legacy Docs path — only when graph mode is not selected

## Discover both connectors

Inspect actual Google Drive folder/search/metadata/create capabilities and Google Docs body read/create/edit capabilities. Use available tool discovery before declaring either missing. If Drive is missing, say briefly that it is needed to find and organize memories and ask the user to connect Google Drive in Claude's connector controls. If Docs is missing, explain briefly that Google Docs is needed to read and write memories and ask them to connect it. If both are missing, identify both in one concise request. Host labels vary; do not invent an exact settings path. After connection, resume the already authorized task, not a new approval flow.

Optional capability discovery: a Docs required-revision argument and returned document revision, atomic create-with-body, placement, and trash for disposable probes. Lack of revision controls does not block setup or learning; use the non-destructive fallback in STORAGE.md. Do not confuse Docs revision control with Drive etag. Access to the same verified IDs through both connectors is what matters, not matching guessed email addresses.

## Quiet bootstrap

Find unique non-trashed config_plugins directly under the connected My Drive root using actual root/ownership evidence and all pages. Find its unique child `yori_2d970fa0-89e4-451e-802b-9f836f99d9e1.json`. Preserve that name/UUID. Read nonempty description config when available; otherwise read its actual body. Omitted description is unknown, not empty. If the field cannot be returned, inspect a body config but do not silently override a potentially conflicting metadata pointer: resolve the existing installation's representation before writes. Malformed or contradictory pointers stop, not fallback to a new Cortex. Validate [schema](../../schemas/config.schema.json). schema_version stays 1; storage_format additionally supports sheets-graph-v1 with cortex_schema_version 1 and a verified spreadsheet ID. Absence is legacy/undetermined, never permission to assume empty memory.

Verify exact selected Cortex and unique Self/People/Knowledge/History children by IDs/parents. Check access; reuse existing records. A read-only user can recall but cannot write. No silently recreated folders/config after a permission error. Resolve once per fresh chat and share results; no repeated probes, README scans or full migration on every learning turn.

## Authorized setup

Account email identification is optional. A request to create a folder authorizes setup through completion with the existing connections. No “Shall I use it?” or routine account-confirmation gate. Ask about an existing folder versus creating one only if not already answered. Show no URL by default. Explain sharing once as information, not another permission ritual; never change permissions.

Create only the selected Cortex and missing Self, People, Knowledge, History folders. The Cortex has NO setup README and no permanent setup_probe. config_plugins may contain the readable developer guide under [README maintenance](../../README_MIGRATION.md). Create the [initial Self](../../templates/initial-self.md) as a readable Google Doc body only if absent, with placement and body read-back. Existing Self is reused. Never import original Yori memories.

Create the fixed configuration using [example](../../templates/config.example.json), replacing its folder placeholder and label. This small configuration may remain JSON in description if supported; otherwise use the config document body. Do not store conflicting copies. New config specifies docs-v2. Read back the chosen representation and actual parent before declaring setup complete. Config is administrative data, not a semantic memory document.

No routine probe is necessary: verified legitimate initial document creation/read-back and the user-tested edit capability establish the normal path; observe actual edit outcomes when needed. If diagnosing an uncertain capability requires a disposable probe, create it outside the Cortex with no personal memory, edit and verify, then trash that exact ID if supported. If cleanup is unavailable, disclose its location once; do not leave probes among memories or permanently delete unknown files.

After verified successful setup, acknowledge readiness naturally. If the name is unknown, ask “What should I call you?” or an equivalent natural question. Then stop. Otherwise finish without a generic follow-up. Use [person matching](../../references/self-continuity.md) on the reply. Explain only an actual unresolved blocker.

## Existing installations

Retain all config/Cortex IDs, Self, people, knowledge and history. Follow [migration](../../MIGRATION.md) for description memories. Installation alone does not operate on Drive or silently bulk-convert a Cortex. Offer the readable-memory upgrade briefly when legacy storage is discovered; get scope authorization for that actual Cortex, then carry the authorized migration through without per-record permission rituals. Optional revision features are not a blocker; unsafe individual conversion paths remain pending while readable records and new learning continue. Never rewrite old test memories to satisfy expectations.

Before person-specific recall or attribution, follow [participant recognition](../../references/participant-recognition.md). Use a grounded account mapping or sole-participant conversational default naturally; no routine identity-verification greeting. Shared ambiguity must not disclose personal history. Reuse the same People identity and record the actual attribution basis.

Apply [source fidelity](../../references/source-fidelity.md): retrieve the relevant current record before established-memory claims; distinguish saved evidence from present interpretation and new reasoning. Preserve business attribution/decision status and ground precise time language. Never learn a new paraphrase or inferred motive as though it were previously stated.
