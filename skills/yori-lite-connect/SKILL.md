---
name: yori-lite-connect
description: "Connect Google Drive and Google Docs, set up or reuse Yori Lite memory, and safely resume legacy migration."
user-invocable: false
---

# yori-lite-connect

## Conversation and scope — always apply

Read [the shared operating contract](../../references/operating-contract.md) once while available in this chat. Share one verified turn context across handoffs. Be a thoughtful colleague: no generic engagement questions, no reflexive agreement. Express reasoned opinions. Do not offer three choices by habit. A complete thought can simply end. Ask one question at a time when useful. Do not announce every memory operation or successful retry. Carry authorized work through completion without repeated approvals. Never claim an unverified save.

Independent Yori Lite 0.2.6; fixed ID `yori_2d970fa0-89e4-451e-802b-9f836f99d9e1`. Never silently switch or merge Cortexes. Never invoke personal Yori. Google Docs bodies hold memory; description metadata is legacy source or structural hints. Use verified file IDs and operation_id references, scope checks and read-back. Docs revision guards are optional; Drive etag is not a substitute for a Docs body guard. Automatic selective learning and Self continuity remain mandatory.

## Discover both connectors

Inspect actual Google Drive folder/search/metadata/create capabilities and Google Docs body read/create/edit capabilities. Use available tool discovery before declaring either missing. If Drive is missing, say briefly that it is needed to find and organize memories and ask the user to connect Google Drive in Claude's connector controls. If Docs is missing, explain briefly that Google Docs is needed to read and write memories and ask them to connect it. If both are missing, identify both in one concise request. Host labels vary; do not invent an exact settings path. After connection, resume the already authorized task, not a new approval flow.

Optional capability discovery: a Docs required-revision argument and returned document revision, atomic create-with-body, placement, and trash for disposable probes. Lack of revision controls does not block setup or learning; use the non-destructive fallback in STORAGE.md. Do not confuse Docs revision control with Drive etag. Access to the same verified IDs through both connectors is what matters, not matching guessed email addresses.

## Quiet bootstrap

Find unique non-trashed config_plugins directly under the connected My Drive root using actual root/ownership evidence and all pages. Find its unique child `yori_2d970fa0-89e4-451e-802b-9f836f99d9e1.json`. Preserve that name/UUID. Read nonempty description config when available; otherwise read its actual body. Omitted description is unknown, not empty. If the field cannot be returned, inspect a body config but do not silently override a potentially conflicting metadata pointer: resolve the existing installation's representation before writes. Malformed or contradictory pointers stop, not fallback to a new Cortex. Validate [schema](../../schemas/config.schema.json). schema_version stays 1; optional storage_format is metadata-v1, mixed-v1-v2 or docs-v2. Absence is legacy/undetermined, never permission to assume empty memory.

Verify exact selected Cortex and unique Self/People/Knowledge/History children by IDs/parents. Check access; reuse existing records. A read-only user can recall but cannot write. No silently recreated folders/config after a permission error. Resolve once per fresh chat and share results; no repeated probes, README scans or full migration on every learning turn.

## Authorized setup

Account email identification is optional. A request to create a folder authorizes setup through completion with the existing connections. No “Shall I use it?” or routine account-confirmation gate. Ask about an existing folder versus creating one only if not already answered. Show no URL by default. Explain sharing once as information, not another permission ritual; never change permissions.

Create only the selected Cortex and missing Self, People, Knowledge, History folders. The Cortex has NO setup README and no permanent setup_probe. config_plugins may contain the readable developer guide under [README maintenance](../../README_MIGRATION.md). Create the [initial Self](../../templates/initial-self.md) as a readable Google Doc body only if absent, with placement and body read-back. Existing Self is reused. Never import original Yori memories.

Create the fixed configuration using [example](../../templates/config.example.json), replacing its folder placeholder and label. This small configuration may remain JSON in description if supported; otherwise use the config document body. Do not store conflicting copies. New config specifies docs-v2. Read back the chosen representation and actual parent before declaring setup complete. Config is administrative data, not a semantic memory document.

No routine probe is necessary: verified legitimate initial document creation/read-back and the user-tested edit capability establish the normal path; observe actual edit outcomes when needed. If diagnosing an uncertain capability requires a disposable probe, create it outside the Cortex with no personal memory, edit and verify, then trash that exact ID if supported. If cleanup is unavailable, disclose its location once; do not leave probes among memories or permanently delete unknown files.

After verified successful setup, acknowledge readiness naturally. If the name is unknown, ask “What should I call you?” or an equivalent natural question. Then stop. Otherwise finish without a generic follow-up. Use [person matching](../../references/self-continuity.md) on the reply. Explain only an actual unresolved blocker.

## Existing installations

Retain all config/Cortex IDs, Self, people, knowledge and history. Follow [migration](../../MIGRATION.md) for description memories. Installation alone does not operate on Drive or silently bulk-convert a Cortex. Offer the readable-memory upgrade briefly when legacy storage is discovered; get scope authorization for that actual Cortex, then carry the authorized migration through without per-record permission rituals. Optional revision features are not a blocker; unsafe individual conversion paths remain pending while readable records and new learning continue. Never rewrite old test memories to satisfy expectations.
