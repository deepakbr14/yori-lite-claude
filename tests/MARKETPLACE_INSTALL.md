# 0.2.6 readable Docs — distribution verification

Release commit 9f7c3e6 was published to deepakbr14/yori-lite-claude. Official Claude CLI 2.1.197 in an isolated temporary configuration successfully refreshed the GitHub marketplace and explicitly upgraded yori-lite from 0.2.5 to 0.2.6. Plugin listing confirmed enabled version 0.2.6. All 19 manifest/skill/schema/template/reference files matched release source byte for byte.

Official manifest validation and ZIP integrity/source-parity checks passed. The CLI retained its existing warning that it ignores the manifest metadata extension; fixed configuration identity also appears in the schema and Skills. No private user installation was changed.

This verifies distribution, not live onboarding or Google connector operations. The user reported actual Claude Drive/Docs creation, reading, editing existing bodies and read-back worked. Full released-plugin lifecycle, two-user concurrency, migration, Docs visual display and latency remain live tests in LIVE_026.md. No Drive/Cortex data or original Yori was modified during this build.
