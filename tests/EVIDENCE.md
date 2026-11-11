# Evidence for 0.2.6 — Google Docs bodies

## User-reported actual-Claude result

The user confirmed Google Drive and Google Docs creating, reading, editing existing document contents and verifying read-back all worked. This supersedes the earlier blocked design. It is sufficient to proceed with the readable-body architecture; it is not a test of strict concurrency controls, full migration or the released Skills.

## Implementation and local validation

Five Skills now use readable Google Docs for semantic memory and Drive for scope/configuration/organization. Both connectors are required and onboarding guides a missing connection. Revision guards are optional: when unavailable, verified readable addenda retain learning without destructive baseline edits. Same config UUID/filename and four memory folders; optional storage_format accepts legacy/mixed/docs-v2. No backend, custom MCP, database or graph was added.

Local tests include legacy regression/protocol models, new claim/History integrity fault models and Docs body/migration models. They exercise snapshots, conflicting writes, no-guard addenda, two contributors, immutable History, stable logical IDs, interrupted/resumed migration, divergent bodies, changed legacy sources and preservation of later Docs learning. They are NOT a Claude model run or actual connector execution. Structured test claims cannot prove correct interpretation of real conversation.

The full lifecycle, rendered Google Docs appearance, actual migration, fresh-conversation recall, two-user guard behavior and latency remain live acceptance in LIVE_026.md. No Drive operations were executed by this build agent and no existing memory/test data was repaired. Original Yori was not accessed or changed. The user-provided capability result is not presented as an independently reproduced test.

No atomic multi-file transactions, server-enforced History immutability or parent isolation are claimed. Unguarded initial creation/migration-mirror races and ambiguous create outcomes remain explicit limits; uncertain completion is not authority. Provider IDs identify records; no generated-looking manual codes. Without safe config marker editing, per-record receipts determine mixed authority.

Package and GitHub upgrade results: LOCAL_CHECKS.txt and MARKETPLACE_INSTALL.md. Instruction byte figures cover a partial scope only and are not latency claims.
