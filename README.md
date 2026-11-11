# Yori Lite for Claude 0.2.7

Yori Lite keeps developing memories in readable Google Docs, organized by Google Drive. It is an independent Skills-only plugin: no server, custom MCP, database or development tools. It does not use the original personal Yori.

## Install and connect

Add [deepakbr14/yori-lite-claude](https://github.com/deepakbr14/yori-lite-claude) through Claude's plugin marketplace repository option and install Yori Lite. Confirm version 0.2.7 and start a fresh chat. Use `/yori-lite`, select its skill, or use the namespace fallback in ENTRY_POINTS.md. Add “setup” if needed.

Connect **both Google Drive and Google Docs** in Claude. Drive finds and organizes the Cortex; Docs reads and edits memories. Yori checks the actual tools and guides you to whichever connection is missing. She uses the existing account without demanding its email. After you authorize a new folder she completes setup without another permission ritual, then naturally asks what to call you if unknown. People with folder access can access its memories.

## Human-readable memory

Self, People, Knowledge and History remain separate folders in the selected Cortex. Memory bodies have useful headings, context, reasons, attribution, references and uncertainty. Main semantic memory no longer goes in descriptions. Stable config_plugins filename and plugin UUID are unchanged. No Cortex README or permanent setup probe is created.

Automatic selective learning remains active. Yori recalls Self before identity claims, distinguishes established preferences from deliberate revisions or uncertain recall, and learns her own considered choices. She can disagree and reconsider. Person identity is not inferred from a shared folder or account owner.

History is append-only by instruction. Before a current-memory change, preserve the prior state and verify new evidence. Use actual Docs revision guards when available. Without them, verified readable addenda preserve new learning without overwriting the baseline; recall includes them. This may leave several readable documents until safe consolidation is available. It is not an atomic transaction or protection against external editors.

## Existing Cortexes

Installation alone does not migrate Drive data. On discovering old description-based memory, Yori offers a scoped readable-memory upgrade. MIGRATION.md specifies source preservation, verification, resume receipts and mixed-format authority. Safe guarded filling retains native Doc IDs; when that is unsafe, a verified readable mirror retains the original logical identity and source link. Conflicts stay pending, not overwritten. No automatic cleanup of old test memories.

The user reports actual Claude Docs creation, reading, editing and read-back passed. The full 0.2.7 lifecycle, migration and two-user tests have not run in this build environment. See tests/EVIDENCE.md and tests/LIVE_026.md for exact limits and test steps. No response-speed improvement is claimed.

## Recognizing returning participants

A sole known participant can be greeted naturally without repeated identity questions; that is a conversational default, not authenticated identity. Where the actual host exposes an account identifier and a grounded person association exists, Yori reuses the mapping in the existing People document. Connected Google account, Claude account and human speaker remain distinct. Shared ambiguity uses a neutral greeting and a brief question only when the task needs identity, without first disclosing personal history. Actual Claude identity-tool availability remains unverified; see tests/IDENTITY_027.md.
