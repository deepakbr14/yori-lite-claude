# Marketplace verification — 0.2.3

Public repository: https://github.com/deepakbr14/yori-lite-claude
Marketplace: yori-lite-claude. Plugin: yori-lite.

On 2026-11-10, release commit `fbcb551` was tested with official Claude Code CLI 2.1.197 in an isolated temporary configuration. `plugin marketplace update yori-lite-claude` fetched GitHub successfully. `plugin update yori-lite@yori-lite-claude` explicitly reported upgrade from 0.2.2 to 0.2.3. `plugin list --json` confirmed 0.2.3, enabled. All 17 installed manifest/skill/schema/template/reference files matched published source byte for byte.

Official validation passed with the existing warning that this CLI ignores the manifest metadata extension. Plugin identity is independently present in the unchanged configuration schema and Skills. Source ./ and marketplace identity are unchanged. ZIP validation also passed.

These results verify the GitHub CLI upgrade route, not Claude.ai sync, chat behavior or Google connector operations. No personal Claude installation, original Yori or real Drive data was touched. Seven live behavior and memory-survival scenarios remain in BEHAVIOR_023.md.
