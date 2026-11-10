# Marketplace verification — 0.2.1

Repository: https://github.com/deepakbr14/yori-lite-claude (public).
Marketplace: yori-lite-claude. Plugin: yori-lite. Expected version: 0.2.1.

Plugin and marketplace names, source ./, fixed config UUID and schema are unchanged. The official Claude Code 2.1.197 validator passed with its existing warning that custom plugin.json metadata is ignored. The config identity remains explicit in schema and skills.

Observed 2026-11-10 against release commit 96a9907, using official Claude Code 2.1.197:

- PASS: fetched public GitHub marketplace with Git global/system config disabled and terminal prompts disabled.
- PASS: isolated installation explicitly updated from 0.2.0 to 0.2.1.
- PASS: plugin list reports yori-lite@yori-lite-claude version 0.2.1, enabled.
- PASS: installed skills/templates/schema and STORAGE.md, README_MIGRATION.md and TURN_EFFICIENCY.md match release source bytes.
- PASS: actual readable-body README template is present in the installed package.

Test configuration was /tmp/yori-lite-020-marketplace, not the user's personal installation. This verifies the GitHub CLI upgrade route, not an actual Drive migration or Claude.ai UI sync. Commands were marketplace update yori-lite-claude, plugin update yori-lite@yori-lite-claude and plugin list --json, all with isolated CLAUDE_CONFIG_DIR.

Claude.ai UI sync is NOT verified from this Codex session. It previously stalled for the user. A CLI installation result must not be presented as proof of Claude.ai sync, UI controls, README rendering, or live Google memory behavior. Verify displayed version 0.2.1 before testing the new chat behavior.

No personal Yori installation or Drive data is touched by these isolated developer installation tests.
