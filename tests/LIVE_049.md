# 0.4.9 live evidence (2026-11-18)

Fresh Claude sessions that could read ONLY `skills/yori-lite/` (simulating a Claude surface that loads just the skill folder). Real Google Drive/Sheets connectors, account enupgames@gmail.com, disposable sandbox folder `1ehfBlNVlXse7xU7hvG-afwE2ZwEggsig`. No real Cortex touched.

- **First-time setup** ("/yori-lite hi"): created Yori Lite folder, Library, Cortex spreadsheet with Memory/Self/Current tabs, config_plugins with README and the settings file (JSON in content and description); read back clean. Reply was only the formatted setup message ending "What should I call you?". About 14 tool calls. Gaps it reported were fixed in the instructions (Library row kind, apostrophe rule for every tab, settings read-back via description, seen_version at setup, page-count wording, person node subject).
- **Google Sheets not connected**: created nothing; reply "**I need Google Sheets connected first.** Connect it, then start a new chat. Nothing was created." plus the Customize → Connectors path. No connector-card tool existed in that test environment, so the card path itself is untested.
- **Cortex the account can't open** (the disposable copy had been deleted): plain formatted message, nothing created, answered the next question with "I don't know… I won't guess."
- **What's new**: person whose seen_version said 0.4.8 got the formatted 0.4.9 note first, then her open question from last time; seen_version saved as 0.4.9; next turn normal (closed the open thread, opened a new one, gave a view).
