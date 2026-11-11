# Identity investigation — 0.2.7

## Verified here (Codex, NOT Claude)

Inspected the actual exposed `google_drive_get_profile` tool: no required arguments, described as returning the current Google Drive user's profile. One read-only call succeeded and returned fields `id`, `email`, `name`, `nickname`, `picture`, `workspace_id`, `workspace_name`, `workspace_picture`. No account values are published in this repository. No Cortex files were read or written for the check.

This establishes an account identifier/address is exposed by this Codex connector in this session. It does not verify Claude exposes the same tool, whether an opaque ID has the same namespace in another connector, cross-chat stability, or who is typing. Display name and a file's owner are not current-speaker authentication. There is no Claude account identity tool available to this session.

## Official documentation, not runtime evidence

[Claude Google Workspace connectors](https://support.claude.com/en/articles/10166901-use-google-workspace-connectors) distinguishes connected Google account access and available Workspace actions. It does not establish a stable current-user field returned to this particular Claude chat.

[Claude Code skill documentation](https://code.claude.com/docs/en/skills) describes skill invocation and host-specific capabilities. The inspected documentation is not evidence of an authenticated Claude.ai account identifier available inside a Skill. No such identity signal was verified in the target Claude runtime. Absence of verification is not a claim that no deployment can expose one.

## Confirmed instruction gap and implementation

0.2.6 distinguished account access from a human and warned against guessing, but did not specify a sole-participant conversational default. That can encourage unnecessary re-identification. The reported awkward greeting was not independently reproduced.

0.2.7 adds a default for one evidenced participant, with no account lookup requirement, identity caveat or repeated sharing explanation. It remains inferred/contextual. Actual connector-authenticated account signals can be associated with an existing People logical ID only when the person linkage is grounded; same-account recognition is not verified-human identity. Conflicting/shared keys stay ambiguous, and explicit guest/correction evidence overrides defaults.

Shared ambiguity never combines personal-history disclosure with “I don't know who is speaking.” Generic conversation does not require a question; person-dependent attribution may. Unknown-speaker learning and Self learning remain active.

## Still requires actual Claude

Use LIVE_027.md to inspect real available identity-tool definitions/results and exercise fresh conversations. We cannot report a Claude ID/email/profile capability as verified based on Codex's tool. The plugin dynamically checks when useful and still works when no identity signal exists. No authentication backend or stronger security guarantee was introduced.
