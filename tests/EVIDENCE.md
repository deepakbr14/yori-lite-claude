# Evidence for 0.2.0

## User-reported live experiments (not rerun by Codex)

The supplied 0.2 request reports: metadata description updates succeeded through 16,000 characters; stale etags were rejected on guarded updates; moving between folders worked; a move alone did not change etag; duplicate names are allowed. Existing file contents cannot be edited through the tested connector. Raw tool transcripts were not supplied. Description search was not established. These facts motivated the architecture and are not claimed as new verified results from this build.

## Local verification

See LOCAL_CHECKS.txt and the output of tests/test_metadata_protocol.py. These are a bounded Python model of the intended protocol, not a plugin runtime, Google connector implementation, or test of Claude's actual skill adherence. They exercise conflict preservation, correction history, ambiguous success, guard absence, failed History verification, same-name creation and unchanged-etag moves.

## Actual Claude chat operations

NOT RUN in this Codex session: first-time conversation; config discovery; metadata learning and cross-chat recall; guarded connector writes; two-person shared learning; corrections/Self retrieval; actual simultaneous writes; ordinary-chat skill activation. No authenticated Claude chat UI/connector control is available here. No substitute Codex/Google API operation is used as proof. tests/FRESH_CHAT.md is the acceptance protocol.

## Installation

Anonymous fresh GitHub installation of 0.2.0 and isolated upgrade from 0.1.0 both passed. Installed source bytes match. Detailed checks are reported in MARKETPLACE_INSTALL.md separately from conversation/connector behavior. No Drive memory was created or modified during this code build. Existing personal Yori files, services and Cortex were neither edited nor invoked.
