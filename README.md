# Yori Lite for Claude

Experimental version 0.1.0, implementing the focused v0.6 brief. A separate skills-only Claude plugin with autonomous selective learning in one Google Drive Cortex. No Yori server, custom MCP, Apps Script, Viewer or personal-Yori dependency.

## Install from GitHub (primary distribution)

1. In Claude.ai or Claude Desktop chat, open **Customize > Plugins > Add marketplace > Add from a repository** (the Add menu may contain Add marketplace).
2. Enter `deepakbr14/yori-lite-claude` or `https://github.com/deepakbr14/yori-lite-claude`.
3. Open the **yori-lite-claude** marketplace and install **Yori Lite** (`yori-lite`).
4. Start a new chat, select **yori-lite** through the `/` or `+` skill picker, or say **Use Yori Lite and help me set up a test Cortex.** If both Yori products are installed, explicitly say Yori Lite.
5. Provide a disposable Google Drive folder link. Setup checks actual Drive/Docs capabilities and one-time group consent. Installing the plugin does not grant Google access.

The repository is PRIVATE. Your Claude GitHub integration must be able to fetch it; a local `gh` login does not grant the Claude service access. Anonymous customers cannot install this private repository just by knowing its URL. Organization marketplace restrictions may also block it. If Claude reports unavailable/unauthorized, inspect its GitHub authorization and repository access rather than making the repository public.

Anthropic documents private GitHub organization sync for Team/Enterprise via **Organization settings > Plugins & skills > Marketplaces > Sync from GitHub**, using the Claude GitHub App installed on this repo. That is a distinct route from personal Add from a repository; do not assume one proves the other. See [marketplace testing](tests/MARKETPLACE_INSTALL.md) for the exact observed coverage and limitations.

The marketplace catalog lives in `.claude-plugin/marketplace.json`; its single `source: "./"` entry resolves to the plugin in this same GitHub checkout. Plugin identity, fixed config UUID and Cortex settings remain unchanged. No second private source repo is needed. GitHub is the intended distribution; ZIP upload is only an optional testing fallback.

If you previously installed the ZIP, avoid enabling two copies of Yori Lite concurrently. If Claude lists a separate uploaded copy, disable/remove only that Yori Lite copy, then install from the marketplace. Never remove personal Yori. Drive config and memory remain independent of installation method.

## Optional ZIP fallback

Upload `yori-lite-0.1.0.zip` through Customize > Plugins for isolated testing. The ZIP deliberately excludes the marketplace catalog; it contains one plugin. Continue with step 4 above. No customer ZIP download is required for the intended repository route.

What Yori retains is shared with those permitted to read that Cortex's files. After this one-time choice, ordinary useful learning does not require a steward approval. Claude may still prompt for tool authorization. Nothing runs in the background.

## What's included

Five skills: conversation, connection/bootstrap, recall, selective learning, organization. Templates and config schema support the proposed visible `config_plugins` convention. Fixed plugin UUID: `2d970fa0-89e4-451e-802b-9f836f99d9e1`. Exact config filename: `yori_2d970fa0-89e4-451e-802b-9f836f99d9e1.json`.

Knowledge is synthesized from durable evidence, not an endless transcript. Without verified atomic conditional edits, the plugin uses separately created History events and optional derived snapshots. Self evolves through revision events. Existing shared documents are not overwritten merely because they were read recently.

## Test status

This is ready for user testing, not claimed working end-to-end. Local checks cover package structure, JSON/YAML, references and contract consistency. This Codex session cannot operate your actual Claude chat Google connectors. GitHub marketplace add/install passed in an isolated Claude Code test. Claude.ai UI installation, bootstrap, unprompted invocation, shared recall and concurrent edits remain NOT RUN until observed. See tests/EVIDENCE.md and tests/CONNECTOR_LOG_TEMPLATE.md.

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
