# Marketplace verification — 0.2.0

Repository: https://github.com/deepakbr14/yori-lite-claude (public).
Marketplace: yori-lite-claude. Plugin: yori-lite. Expected version: 0.2.0.

The catalog uses source ./, preserving existing marketplace/plugin identity and the fixed config UUID. No custom connector or second repository is needed. GitHub distribution remains primary.

Local official CLI validation passed with one warning: Claude Code 2.1.197 ignores the custom metadata field in plugin.json. The actual config identity is also explicit in skills and schema, so it does not depend on that host field.

Remote tests on 2026-11-10 against release commit 7cc7f32, using official Claude Code 2.1.197:

| Experiment | Observed result |
| --- | --- |
| Fresh HTTPS GitHub marketplace add, with Git global/system config disabled and terminal prompts disabled | PASS, anonymous public repository clone and marketplace registration |
| Install yori-lite@yori-lite-claude into isolated temporary config | PASS, enabled version 0.2.0 |
| Installed skills, templates, schema and STORAGE.md byte comparison | PASS, match release source |
| Refresh prior isolated 0.1.0 marketplace and run plugin update | PASS, CLI explicitly reported updated from 0.1.0 to 0.2.0 |
| Actual Claude.ai UI / live Google metadata operations | NOT RUN, no authenticated Claude chat control in this session |

Fresh installation used /tmp/yori-lite-020-marketplace. Upgrade used the earlier /tmp/yori-lite-marketplace-test-config test installation, not the user's personal Claude setup. No Drive content or personal Yori was touched. These install results do not establish conversational behavior or live connector adherence.

To update in Claude: refresh/re-sync the yori-lite-claude marketplace, update Yori Lite, confirm version 0.2.0, and open a new chat. If an old ZIP-installed copy is separately enabled, disable only that duplicate Yori Lite copy. Do not remove personal Yori or delete any Drive data.

The earlier authenticated 0.1.0 CLI install test remains in Git history; it is not evidence of 0.2 connector behavior.
