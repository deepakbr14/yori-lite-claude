# 0.2.7 distribution verification

Release d1bb546 published to deepakbr14/yori-lite-claude. Official Claude CLI 2.1.197, using an isolated temporary configuration, refreshed the GitHub marketplace and explicitly upgraded yori-lite from 0.2.6 to 0.2.7. Listing confirmed enabled version 0.2.7. All 21 manifest/skill/schema/template/reference files matched release source byte for byte.

Package/ZIP validation passed. Official manifest validator passed with the existing warning that its metadata extension is ignored by this CLI; fixed config identity is also in schema and Skills. This does not prove Claude.ai runtime identity exposure or conversational behavior.

84 local tests passed, including 17 recognition cases. One actual Codex read-only Google profile check returned ID/email/name fields; this is not a Claude connector check. Actual Claude identity-tool inspection and all five live conversation scenarios remain in LIVE_027.md. Existing Cortex data and original Yori were untouched.
