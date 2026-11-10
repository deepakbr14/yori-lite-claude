# Marketplace verification — 0.2.0

Repository: https://github.com/deepakbr14/yori-lite-claude (public).
Marketplace: yori-lite-claude. Plugin: yori-lite. Expected version: 0.2.0.

The catalog uses source ./, preserving existing marketplace/plugin identity and the fixed config UUID. No custom connector or second repository is needed. GitHub distribution remains primary.

Local official CLI validation passed with one warning: Claude Code 2.1.197 ignores the custom metadata field in plugin.json. The actual config identity is also explicit in skills and schema, so it does not depend on that host field.

Remote 0.2.0 install/update result will be recorded after the release commit is fetched through GitHub. This is separate from actual Claude.ai chat testing, which is NOT RUN in this Codex session. No authenticated Claude.ai browser control is available.

To update in Claude: refresh/re-sync the yori-lite-claude marketplace, update Yori Lite, confirm version 0.2.0, and open a new chat. If an old ZIP-installed copy is separately enabled, disable only that duplicate Yori Lite copy. Do not remove personal Yori or delete any Drive data.

The earlier authenticated 0.1.0 CLI install test remains in Git history; it is not evidence of 0.2 connector behavior.
