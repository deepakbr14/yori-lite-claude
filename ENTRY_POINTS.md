# Yori Lite entry point

The main skill's stable name is `yori-lite`. It handles conversation and first-time setup. Explicit setup is `yori-lite` with the message “setup”; valid existing settings are checked and reused, not reset. The long connect skill is an internal procedure, not the default command users need to discover.

The existing five skill identities are retained for compatibility. The four helpers have `user-invocable: false` so hosts honoring that field keep them out of the user slash menu while the model can still use them. No duplicate commands/yori-lite.md or invented manifest alias is added. No /yori alias is registered, avoiding collision with personal Yori.

Claude Code's current official skill naming documentation says plugin skills have canonical `/plugin-name:skill-name` names and also support the bare skill name when not claimed by another command. Thus `/yori-lite` is the preferred short invocation and `/yori-lite:yori-lite` is the explicit namespace fallback. `/yori-lite setup` expresses setup intent on a host accepting that short name. Do not rename the plugin to get a shorter command.

In Claude.ai/desktop chat, choose `yori-lite` from the slash or + skill picker if typing the short name does not invoke it. Actual slash display, helper hiding and short-alias resolution must be tested in the target chat; CLI packaging validation alone does not establish that behavior. Natural language “Use Yori Lite to set up my memory folder” remains supported intent.

Official references checked for 0.2.2:
- https://code.claude.com/docs/en/skills#how-a-skill-gets-its-command-name
- https://code.claude.com/docs/en/skills#control-who-invokes-a-skill
- https://support.claude.com/en/articles/13837440-use-plugins-in-claude
