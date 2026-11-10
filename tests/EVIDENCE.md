# Evidence for 0.2.2

## User-reported, not rerun here

Setup and metadata memory creation worked in live Claude tests. Earlier experiments reportedly reached 16,000-character descriptions, rejected stale guarded etags, permitted moves without changing etag, and allowed duplicate filenames. Existing file contents could not be edited through that connector. Description search remains unverified.

The latest Aurora conversation reportedly took about 32 seconds, including contribution and topic creation. An earlier run was about 35 seconds. No tool traces or per-operation timings were supplied; this is not a controlled speed comparison.

## Measured locally

INSTRUCTION_SIZE.json records UTF-8 file bytes: 43,817 bytes across five previous skills versus 26,334 bytes across the new skills plus 7,295 bytes in their shared contract (33,629 total). This is about 23% less text for that defined scope, not a token estimate or measured response speed. Other task-specific supporting documents are excluded.

Local instruction/metadata models cover conflict history, retry safety, README preservation and narrowly guarded guide retirement. These models are developer checks, not executable plugin enforcement or live Claude behavioral tests. Tests involving marked/unmarked/changed guides use disposable in-memory fixtures only.

## Platform naming

Official Claude skill docs describe plugin namespaces and bare-name invocation when no conflict exists. yori-lite remains the main skill; helpers are model-available and marked non-user-invocable. No duplicate command file or /yori alias is added. Actual Claude.ai picker/alias handling and helper visibility still require live validation. See ENTRY_POINTS.md.

## Live limits

NOT RUN here: 0.2.2 chat setup, authenticated account detection, Drive README visual display, actual guarded trash, ordinary conversation/curiosity, two-account learning, or new response-time measurements. No authenticated Claude.ai UI or its Google connector control is available to this Codex session. No personal Yori or Drive data was accessed or modified during the build.

GitHub CLI installation results are recorded separately in MARKETPLACE_INSTALL.md; they do not prove Claude.ai UI sync or live memory behavior.

Additional verified release checks: official Claude CLI validator passed with the existing ignored-metadata warning; seven configuration/schema, memory-template and marketplace files remained byte-identical to 0.2.1. Isolated GitHub marketplace upgrade from 0.2.1 to 0.2.2 passed, with installed source-byte parity. See MARKETPLACE_INSTALL.md.
