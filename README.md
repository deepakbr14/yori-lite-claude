# Yori Lite for Claude 0.2.0

Yori learns, remembers and revises her understanding through the descriptions of files in one Google Drive folder. File contents can be empty. She chooses useful memories naturally, with a developing Self and preserved contributor perspectives.

## Install or update through GitHub

In Claude.ai or Claude Desktop chat, open **Customize > Plugins > Add marketplace > Add from a repository**, enter `deepakbr14/yori-lite-claude`, and install **Yori Lite**. The repository is public. If already installed, refresh/re-sync the marketplace and update Yori Lite; verify version **0.2.0** in plugin details. Host UI labels can vary. Start a new chat after updating. No ZIP upload is required.

Say **“Hi Yori Lite”** or select the yori-lite skill. She should ask naturally whether you have a folder for her memories, or offer to create one. Use a disposable folder for this test. She confirms who can see retained information once, then learns without requesting approval for every memory. Claude's tool permission prompts still apply.

If both Yori products are installed, explicitly say Yori Lite when ambiguous. Neither installation method nor version 0.2 contacts personal Yori. The plugin has no custom MCP/server, database, graph, embeddings, Apps Script or Viewer. Only the actual Claude Google Drive connector is used; editing existing file contents is not needed.

## Storage

Self/People/Knowledge hold current memories; History holds immutable meaningful contributions and prior revisions. Knowledge lives in description, usually about 4,000 characters or fewer. The user reports successful 16,000-character tests; this is not a promise for every host. Description search remains unverified, so recall also supports scoped metadata listing.

Each shared description revision uses the connector's actual expected-etag precondition. On conflict, Yori re-reads, reconciles and retries within a small limit. Contributions are retained and verified before changing shared summaries; failures leave recoverable evidence. Merges and splits preserve originals until replacements are verified. Logical retirement is preferred because moving a file does not change its etag. See STORAGE.md for limitations, including external-move races and lack of transactions.

The config_plugins convention and fixed UUID remain stable. New config JSON lives in description. Older body-based config is readable without editing it; no automatic migration or Cortex switching. See CONFIG_PROTOCOL.md and MIGRATION.md.

## Evidence and tests

User-reported live connector results are recorded separately from tests performed by Codex. Local protocol simulations test conflicts, corrections, retry recovery and parent moves; they are NOT live connector validation or proof that a language model follows the skills. Actual Claude chat onboarding, ordinary-chat activation, metadata learning and two-user behavior need the tests in tests/FRESH_CHAT.md. See tests/EVIDENCE.md for exact status.

Developer checks: `python3 tools/check_package.py`, `ruby tools/check_frontmatter.rb`, `python3 -m unittest discover -s tests -p 'test_*.py'`. These developer tools are not a plugin runtime. `python3 tools/package.py` builds an optional test ZIP; GitHub marketplace is primary.

## Remove

Remove only Yori Lite through Claude's plugin controls. This does not delete Drive memory/config or affect personal Yori. Delete disposable test resources only when you intentionally choose to; do not remove a shared Cortex without its group's authorization.

Official platform references checked for this release:
- https://support.claude.com/en/articles/13837440-use-plugins-in-claude
- https://support.claude.com/en/articles/10166901-use-google-workspace-connectors
- https://code.claude.com/docs/en/plugins/host-marketplace

General platform documentation does not override the observed capabilities of the specific connector exposed in your chat.
