# Evidence for 0.2.3

The user reports successful live Cortex setup and memory creation in the preceding release. Those tests were not rerun here.

This release changes conversational instructions and the release version, not storage architecture. All five Skills were reviewed against the seven requested scenarios; BEHAVIOR_023.md records their expected behavior and live test steps. Editorial/static coverage is not proof of model compliance.

Local regression tests exercise metadata conflict/history models, conservative guide handling, package identity and instruction contracts. COMPATIBILITY_023.json records byte-identical storage protocol, scheduling, documentation migration, schema, templates and marketplace versus 0.2.2. Actual saved memories were not accessed, changed or tested.

INSTRUCTION_SIZE.json measures current UTF-8 instruction bytes against the original 0.2.1 baseline, not response time or tokens. No response-time improvement is claimed for this conversational release. Earlier measured 0.2.2 instruction sizes remain in Git history.

Official CLI validation and GitHub upgrade results are in MARKETPLACE_INSTALL.md. These do not verify Claude.ai sync/aliases, live onboarding, quiet retries, real account identity or memory survival. No authenticated Claude.ai/Google connector session is available here. The original personal Yori and real Drive data were not touched.
