# Marketplace verification — 0.2.2

Public repository: https://github.com/deepakbr14/yori-lite-claude
Marketplace: yori-lite-claude. Plugin: yori-lite.

On 2026-11-10, published release commit `7a86f8e` was tested with official Claude Code CLI 2.1.197 in an isolated temporary configuration. The existing test installation was 0.2.1. `plugin marketplace update yori-lite-claude` fetched GitHub successfully; `plugin update yori-lite@yori-lite-claude` explicitly reported upgrade from 0.2.1 to 0.2.2. `plugin list --json` confirmed version 0.2.2, enabled. All installed manifest, skills, schemas, templates and references matched the published source byte for byte.

The official validator passed with one warning: this CLI ignores the existing plugin.json metadata extension. The fixed identity is also present in the configuration schema and skill instructions and does not depend on that extension. Marketplace source ./, plugin identity and config UUID/schema are unchanged. Five skills remain; yori-lite is the primary entry with four internal helpers.

CLI validation/install does not prove Claude.ai command aliases, picker hiding, sync, conversation behavior or Google connector operations. No user personal installation or Drive data was touched by these isolated tests. No response-latency improvement has been measured.
