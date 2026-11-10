# Build evidence

Version 0.1.0 targets the v0.6 build brief. Local package validation is recorded in LOCAL_CHECKS.txt after execution. A subsequent marketplace test downloaded an isolated official Claude CLI, validated the catalog, and installed from authenticated GitHub. See MARKETPLACE_INSTALL.md for observed results, the metadata warning, and remaining Claude.ai UI limitations.

Actual Claude connector operations: NOT RUN. No Claude chat control tool is available to this Codex session. Codex's Google connector is a different host surface and was deliberately not used as evidence of Claude compatibility.

Live installation, config roundtrip, fresh-chat invocation, second-user recall, denied access, conditional revisions and concurrent updates: NOT RUN. tests/FRESH_CHAT.md and CONNECTOR_LOG_TEMPLATE.md define how to gather real outcomes.

Preexisting product files inspected during this build: none. The supplied v0.6 PDF and earlier design context informed the package. Existing personal Yori source, services and Cortex were neither modified nor invoked. All build changes are in this new isolated source directory and its adjacent ZIP.
