# Yori Lite 0.4.0 — FAST Cortex

Yori learns into readable, compact Google Sheets rows. One **Memory** tab stores NODE, EDGE and REVISION records. Facts stay small; relationships, contributor attribution and the history of changes remain intact. No custom MCP, Apps Script, backend, Bash preparation or mandatory Claude Project.

## Install

Use the existing [GitHub marketplace](https://github.com/deepakbr14/yori-lite-claude), install Yori Lite **0.4.0**, then start a fresh Claude chat. A ZIP is also available. New setup guides connection of Google Drive and Google Sheets. Existing Cortex configuration is reused; installing this version never migrates or resets it.

FAST writes use Claude's actual `append_values` shape: short row arrays, one call for related rows, then one small verification read when receipts/coverage allow. No per-cell wrappers, checksums, duplicate History snapshots or commit manifests. Every row carries an operation token, part and total. Missing rows stay pending; retries preserve IDs; competing revisions remain visible.

## Test before switching an existing Cortex

Run [this short Claude test](tests/LIVE_FAST.md) on a disposable workbook. Local and disposable Codex correctness tests have passed, but Claude timing and append semantics still need that test. A representative node-plus-edge request is **423 compact JSON bytes**. This is not a measured latency improvement: under 10 seconds, ideally 3–5, remains a target.

The old five-tab graph and Docs readers remain. After validation and an explicit switch request, FAST can read the old graph as a retained source and link new revisions to its original IDs. No old data needs deletion or bulk conversion. Configuration switching has no assumed CAS; coordinate writers. [Compatibility and rollback](ROLLBACK.md).

## Honest limits

Incomplete/mismatched appends and observed ID collisions are detected; this is not exactly-once delivery, guaranteed unique model-generated IDs or tamper-proof storage. Later well-formed manual edits are not always detectable without hashes. Fresh chats may need an O(N) index scan if Claude lacks exact server search; warm chats reuse maps and refresh the append tail. Source attribution is evidence, not authentication. [Evidence and measurements](tests/FAST_EVIDENCE.md).

Five Skills, unchanged plugin UUID/bootstrap, independent from the original personal Yori. Automatic selective learning, Self continuity, natural conversation and independent judgment stay active. The developer Python verifier is optional offline tooling, not a Claude runtime dependency.

[FAST row format and save procedure](references/fast-cortex.md) · [Legacy graph schema](GRAPH_SCHEMA.md) · [Config protocol](CONFIG_PROTOCOL.md)
