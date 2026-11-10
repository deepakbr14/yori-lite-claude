# Yori Lite for Claude

Experimental version 0.1.0, implementing the focused v0.6 brief. A separate skills-only Claude plugin with autonomous selective learning in one Google Drive Cortex. No Yori server, custom MCP, Apps Script, Viewer or personal-Yori dependency.

## Install and start

1. In Claude.ai or Claude Desktop chat, open Customize > Plugins and upload `yori-lite-0.1.0.zip` without unzipping it. Organization controls may limit uploads.
2. Ensure your approved Google Drive connection is available. Google Docs editing can require its separate connector. Setup inspects actual tools; installing this ZIP grants no Google access.
3. Start a chat and select **yori-lite** through the `/` or `+` skill picker, or say: **Use Yori Lite and help me set up a test Cortex.** If both Yori products are installed, explicitly say Yori Lite.
4. Provide the link to a disposable Google Drive folder you control. Confirm the group disclosure when shown. Setup verifies folder access, creates Self/People/Knowledge/History and the per-user config, and reports any unsupported connector operation.
5. Say something worth retaining, then open a fresh chat and follow tests/FRESH_CHAT.md. No-reminder invocation is a separate experiment; use explicit skill selection as recovery, not proof of automatic loading.

What Yori retains is shared with those permitted to read that Cortex's files. After this one-time choice, ordinary useful learning does not require a steward approval. Claude may still prompt for tool authorization. Nothing runs in the background.

## What's included

Five skills: conversation, connection/bootstrap, recall, selective learning, organization. Templates and config schema support the proposed visible `config_plugins` convention. Fixed plugin UUID: `2d970fa0-89e4-451e-802b-9f836f99d9e1`. Exact config filename: `yori_2d970fa0-89e4-451e-802b-9f836f99d9e1.json`.

Knowledge is synthesized from durable evidence, not an endless transcript. Without verified atomic conditional edits, the plugin uses separately created History events and optional derived snapshots. Self evolves through revision events. Existing shared documents are not overwritten merely because they were read recently.

## Test status

This is ready for user testing, not claimed working end-to-end. Local checks cover package structure, JSON/YAML, references and contract consistency. This Codex session cannot operate your actual Claude chat Google connectors. Actual installation, bootstrap, unprompted invocation, shared recall and concurrent edits remain NOT RUN until observed. See tests/EVIDENCE.md and tests/CONNECTOR_LOG_TEMPLATE.md.

A read-only connector cannot fulfill the learning contract. If ordinary JSON file operations, verified folder scoping or required writes are missing, setup explains the precise blocker; it does not fall back to another service or claim a saved configuration.

## Source and build

Repository: https://github.com/deepakbr14/yori-lite-claude (private test source).
Run `python3 tools/check_package.py`, then `python3 tools/package.py`. Run `ruby tools/check_frontmatter.rb` for YAML parsing. These are developer packaging tools, not plugin runtimes; the install ZIP excludes tools and build output. If Claude Code is installed, additionally run `claude plugin validate . --strict`; this does not prove chat/Google behavior.

## Remove

Remove Yori Lite in Claude's plugin controls. This does not delete Drive memory/config, revoke connectors, or affect personal Yori. Delete only your own disposable test resources manually if desired; do not delete a shared Cortex without its group's authorization.

## Platform references checked 2026-11-10

- https://support.claude.com/en/articles/13837440-use-plugins-in-claude
- https://code.claude.com/docs/en/plugins-reference
- https://support.claude.com/en/articles/10166901-use-google-workspace-connectors

Google Drive search/file management and Google Docs editing are separate capabilities. Actual tool availability, organization policy and permission prompts must be tested in the target chat.
