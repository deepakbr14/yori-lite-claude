---
name: yori-lite-recall
description: "Retrieve current Self, People, Knowledge and graph relationships faithfully, with existing Docs compatibility."
user-invocable: false
---

# yori-lite-recall

## Conversation and scope — always apply

For Sheets mode, use the compact runtime in [main entry](../yori-lite/SKILL.md) and [graph protocol](../../references/graph-cortex.md), reusing them if already loaded. Do not load every Skill or supporting reference for each operation. The [shared operating contract](../../references/operating-contract.md) and legacy references are for Docs mode or a specific unresolved detail, not mandatory graph startup reads. Share one verified turn context across handoffs. Be a thoughtful colleague: no generic engagement questions, no reflexive agreement. Express reasoned opinions. Do not offer three choices by habit. A complete thought can simply end. Ask one question at a time when useful. Do not announce every memory operation or successful retry. Carry authorized work through completion without repeated approvals. Never claim an unverified save.

Independent Yori Lite 0.3.2; fixed ID `yori_2d970fa0-89e4-451e-802b-9f836f99d9e1`. Never silently switch or merge Cortexes. Never invoke personal Yori. Storage routes by the existing config: Google Sheets graph rows in sheets-graph-v1; Google Docs bodies in docs-v2. Description metadata remains config/legacy source. Verify scope, operation_id and read-back. Drive etag is not a body/row compare-and-swap. Automatic selective learning and Self continuity remain mandatory.

## Sheets routing — read before storage operations

When config selects `sheets-graph-v1`, read [graph Cortex protocol](../../references/graph-cortex.md) and follow its role-specific procedure below. Its immutable rows, commit verification and head resolution replace ALL Docs-specific storage instructions in the legacy section. Shared identity, attribution, source-fidelity and conversational rules still apply. For an EXISTING config that selects Docs/legacy or lacks a graph selector, use the existing Docs path; installation never changes the selected store. If no config exists, route to connection for NEW Drive/Sheets setup before requiring Docs. Missing config is not an existing legacy selector. Google Drive discovery, fixed UUID/config filename, folder selection and permissions remain unchanged.

Resolve current full node versions, including competing heads and pending relevant contributions. Use Directory row hints only with node_id/revision_id verification and a complete current-head check. Find incoming/outgoing edges by stable IDs, validate committed active edge versions and endpoints, and traverse one or two hops only when useful. Use bounded reads and complete pagination; do not load the whole workbook every turn. History is evidence, never a substitute for current Self/People/Knowledge. Preserve saved reasons versus present interpretation and temporal uncertainty.

## Legacy Docs path — only when graph mode is not selected

## Current record before historical reconstruction

Follow [source fidelity](../../references/source-fidelity.md) for every memory-backed answer. Identify the subject and fetch the relevant current Self, People or Knowledge body first; don't reconstruct current understanding from a loosely related History hit. Reuse a valid same-turn body. If only History was retrieved, perform a targeted current-folder lookup before claiming to remember. A missing current record remains unconfirmed, not silently replaced by plausible history.

## Scoped body retrieval

Resolve the recognition basis before using person-specific conversational history. Read only the needed recognition/participation evidence; full document reads may contain more, but do not volunteer those personal details while identity is unresolved. Self and general/shared knowledge can be recalled without identifying the speaker.

Resolve exact Cortex and representation first. Read format-2 memory from actual Google Docs bodies, including all relevant tabs/sections and references; do not read an empty export and assume no knowledge. Use metadata for IDs, parents, access and legacy descriptions only. Follow [migration](../../MIGRATION.md) for unconverted or partially converted records. Do not mix a retained stale description over a verified newer body. Missing/truncated fields are unknown. README/probe documents are not semantic memories.

Load Self at fresh-chat activation, including relevant contributions/corrections and body addenda before identity claims. Follow [continuity](../../references/self-continuity.md). Initial Self is not the entire developing identity. Start with bounded relevant documents; expand within scope when needed. Search misses and incomplete listing never establish an unset preference. Do not search another Cortex as fallback.

After retrieving the matching current baseline, read referenced History and relevant pending contributions/addenda needed to resolve its state. If the baseline cannot be read, qualify any supported historical answer as historical only. In the no-revision-guard mode, current documents may have immutable readable addenda with “Updates” source links; include these before stating current understanding. They amend the baseline, not prove automatic supersession by timestamp. Conflicting simultaneous choices remain conflicting until reasoned reconciliation. Referenced source bodies, authorship and actual reasons decide meaning, not the newest filename.

Apply [integrity](../../references/memory-integrity.md): preserve direct statements versus attributed reports versus Yori inferences/decisions and uncertainty. Use neutral wording for unknown attributes. Cite verified document links naturally. Reuse still-valid body reads across Skills, but do not skip content required to understand a revision. Genuine unavailable sources produce a concise uncertainty statement, not fabricated memories.

Before person-specific recall or attribution, follow [participant recognition](../../references/participant-recognition.md). Use a grounded account mapping or sole-participant conversational default naturally; no routine identity-verification greeting. Shared ambiguity must not disclose personal history. Reuse the same People identity and record the actual attribution basis.
