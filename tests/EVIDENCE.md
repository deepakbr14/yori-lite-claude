# Evidence for 0.2.4

The user reported a live 0.2.3 regression after “make one”: Yori demanded account identification before setup. Inspection confirmed mandatory account-identification instructions in the shared contract and setup Skill. These were removed, including the unknown-email fallback question. All five Skills now treat email as optional and prohibit unnecessary questions/progress narration.

No authenticated Claude.ai connector execution is available through this session's tools. The full actual-connector first-time setup test has NOT RUN and is a release acceptance gap. LIVE_SETUP_024.md supplies the exact live sequence, including durable learning and fresh-chat recall. CLI installation and local static/model tests do not establish conversational behavior or connector success.

Storage protocol, schema, templates, marketplace identity and prior guide migration are preserved. No real Drive data or original Yori was accessed or changed. Unknown identity is distinct from permission/scope verification, which remains required. Unknown capability is not declared absent without actual tool evidence.

Local/package results are in LOCAL_CHECKS.txt; GitHub route results are in MARKETPLACE_INSTALL.md. Older scenario/evidence documents are historical, not current instructions. In particular, 0.2.3 account-confirmation expectations are superseded by optional identification in 0.2.4.
