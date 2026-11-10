# GitHub marketplace installation evidence

Tested 2026-11-10 against commit 7bb4f29 using the official npm-distributed Claude Code 2.1.197. Configuration and installation cache were isolated under /tmp/yori-lite-marketplace-test-config. No existing personal Claude installation or Yori plugin was changed.

## Observed results

| Check | Result |
| --- | --- |
| Official marketplace validator | PASS with one warning: this CLI ignores custom plugin.json metadata. Fixed config identity remains in schema and Skills. |
| Remote GitHub repository visibility | PRIVATE; default branch main |
| Anonymous raw marketplace request | HTTP 404, as expected for a private repository |
| Add GitHub marketplace using authenticated Git credentials | PASS: cloned HTTPS repository and registered yori-lite-claude |
| Install yori-lite@yori-lite-claude from downloaded marketplace | PASS: installed version 0.1.0, enabled |
| Installed contents | Manifest and all five SKILL.md files match source bytes |
| Claude.ai Customize > Plugins > Add marketplace > Add from a repository | NOT RUN: no authenticated Claude.ai UI control is available in this Codex session |
| Organization GitHub App sync | NOT RUN: not configured through this session |

This is a real GitHub marketplace add/install test, not a ZIP install or a local-directory marketplace test. It proves CLI ingestion with this user's authenticated Git access. It does not prove the requested Claude.ai UI can authenticate to this private repository.

Commands used (temporary test configuration and credential helper applied only to these commands):

```text
claude plugin validate <repository-directory>
claude plugin marketplace add deepakbr14/yori-lite-claude
claude plugin install yori-lite@yori-lite-claude
claude plugin list --json
```

## Finish the Claude.ai acceptance test

1. In the intended Claude account, open Customize > Plugins > Add marketplace > Add from a repository.
2. Enter deepakbr14/yori-lite-claude.
3. Record whether Claude can fetch the private repository and shows marketplace yori-lite-claude with Yori Lite.
4. Install Yori Lite and confirm its five skills are available. Start a chat and explicitly select yori-lite.
5. Record the exact redacted error if fetch or install fails. Do not infer that valid JSON grants private GitHub access.

The GitHub identity authorized to Claude must have repository access. The terminal gh login used by this test is not Claude's authorization. A customer without authorized repository access cannot install from this private URL; an anonymous fetch was observed to return 404. Company policy can independently restrict marketplaces.

For Team/Enterprise organization distribution, Anthropic documents private repository sync through Organization settings > Plugins & skills > Marketplaces > Sync from GitHub, with the Claude GitHub App installed for the repository. This is a separate documented route, not an observed success of the personal Add from a repository flow. Do not make the repository public to work around an access error without the owner's explicit approval.

The catalog uses source ./, so all plugin files are in the marketplace's own checkout, avoiding another private source dependency. The fixed plugin UUID and config filename are unchanged. The upload ZIP remains a secondary test artifact, not the intended customer distribution.

References checked:
- https://support.claude.com/en/articles/13837440-use-plugins-in-claude
- https://support.claude.com/en/articles/13837433-manage-plugins-for-your-organization
- https://code.claude.com/docs/en/plugins/marketplace-reference
