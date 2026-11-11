# 0.2.8 distribution verification

Release 712e891 published to deepakbr14/yori-lite-claude. Official Claude CLI 2.1.197 in an isolated temporary configuration refreshed the GitHub marketplace and explicitly upgraded yori-lite from 0.2.7 to 0.2.8. Listing confirmed enabled 0.2.8; all 22 manifest/skill/schema/template/reference files matched release source byte for byte.

Package/ZIP validation passed. Official manifest validator passed with the existing ignored-metadata warning. 102 local tests passed. Actual saved Google Docs fixture creation, exact read-back and targeted retrieval were performed through Codex Google tools (REAL_DOCS_028.md), not a fresh Claude conversation.

Full Claude source selection, answer fidelity, independent interpretation and temporal wording remain acceptance tests in LIVE_028.md. No production config was repointed and no experimental/personal Yori memory was repaired. Only the new disposable source fixture was created. Private source IDs/read-backs are excluded from the Git repository and plugin ZIP.
