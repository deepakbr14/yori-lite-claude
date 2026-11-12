# Yori Lite 0.3.0 — Sheets graph Cortex

This five-Skill Claude plugin adds a Google Sheets graph Cortex while retaining the existing Docs path. No custom MCP, hosted backend, Apps Script, new authentication or mandatory Project. It never accesses the original personal Yori.

Version 0.3.0 is distributed through the existing GitHub marketplace. Installation does not migrate memories or change an existing configuration. The established plugin and repository identity are retained.

## Install and test

Add or refresh [deepakbr14/yori-lite-claude](https://github.com/deepakbr14/yori-lite-claude) through Claude’s **Customize → Plugins → Add marketplace → Add from a repository** flow, then install Yori Lite. Confirm version **0.3.0** and start a fresh chat with /yori-lite. Existing marketplace users receive this through the same repository. See ENTRY_POINTS.md for namespacing. A ZIP remains available for manual installation; it is not the primary distribution route.

New setup uses **Google Drive and Google Sheets**. Existing Docs Cortexes still use Drive and Docs unless an explicit migration is requested. Yori inspects actual tools, uses the connected account without requiring its email, and finishes authorized setup. Safe new writes require genuine append and a trusted host/provider UUID generator; an invented identifier is not a substitute.

Follow [the Claude test script](tests/LIVE_GRAPH.md) with an explicitly named disposable workbook to test without changing your saved pointer. The clean supplied workbook/JSON contains ten synthetic nodes and ten edges. Never import these fictional people and amber preference as a real user's initial identity.

## Memory and conversation

Nodes store complete readable memories; Edges store evidence-backed relationships. History preserves contributions, prior states and corrections. Directory contains row hints; Metadata identifies the schema. Stable IDs survive row movement. No graph memory requires opening a Doc.

Writes append immutable versions rather than replacing rows. Two writers' branches remain until explicitly reconciled. Reused operation IDs and exact-payload verification prevent duplicate logical records; this is not exactly-once delivery or a database transaction. Human editors can still corrupt records. A row pointer must be checked against IDs, commits and later versions before claiming current memory.

Selective automatic learning, Self continuity, natural participant recognition and independent judgment remain active. Yori distinguishes saved evidence from new reasoning, retains uncertainty/disagreement, and avoids unsupported attributes or motives. Routine memory operations stay quiet.

## Specifications and migration

- [Schema](GRAPH_SCHEMA.md) and [graph protocol](references/graph-cortex.md)
- [Unchanged bootstrap convention and small extension](CONFIG_PROTOCOL.md)
- [Safe Docs-to-Sheets staging](GRAPH_MIGRATION.md)
- [Rollback preserving graph-only learning](ROLLBACK.md)
- [Benchmarks and limitations](tests/GRAPH_BENCHMARKS.md)

The optional standard-library utility scripts/graph_cortex.py generates fixtures, stages a complete connector-exported Docs snapshot, and audits workbook JSON. It has no network access and is not a hosted runtime. It preserves source content and IDs without fabricating edges or switching config. Baseline/addendum and participant mappings require verification before activation. Oversized/ambiguous records remain blocked with their originals intact.

Local tests and Codex connector results are separate from Claude acceptance. Disposable native workbooks at 10, 1,000 and 10,000 nodes were exercised. Claude's actual tool interface, fresh-chat learning/recall, two authenticated writers, and full migration/rollback still require the supplied live tests. No production readiness claim.
