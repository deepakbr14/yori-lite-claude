# Required actual-Claude acceptance test — NOT RUN

This Codex session has no tool that invokes the authenticated Claude.ai Google Drive connector. Codex Drive tools and Claude CLI package installation are not substitutes. The fix is published for testing, not certified end to end.

Use a disposable Google account/Drive connected to Claude with no existing Yori Lite configuration. Do not disconnect or modify a production Cortex for this test. Verify the installed plugin shows 0.2.4 and start a fresh chat.

Send this first message:

> /yori-lite setup — Let's get you set up. This is a disposable test Drive. Use the Google Drive connection already attached to this chat. Don't change or reset any existing Yori configuration or Cortex; if one already exists, stop this first-time test and tell me. Otherwise ask me whether to create a memory folder.

When Yori asks about a folder, send exactly:

> make one

Observe the ordinary setup without coaching further. Required result: Yori uses the actual exposed connector to create the folder, initializes Self and required folders, writes her configuration pointer, verifies all required results, and acknowledges completion. Unknown email must not trigger an account question. No repeated progress narration, generic follow-up, or unverified capability claims. Host-generated activity/cards do not count as narration.

After completion, send:

> Remember this fictional test fact: Aurora's navigator is Mara.

Start another fresh chat with Yori Lite and ask:

> Who is Aurora's navigator?

Finally ask for evidence:

> For this disposable test, summarize the actual connector operations and their verified outcomes: folder creation, initialization, configuration pointer, read-back verification, and fresh-chat recall. Distinguish observed errors from unknown capabilities. Don't claim an operation ran if it didn't. Don't change or delete anything else.

Record actual client/plugin version, Yori's messages, and connector results. Keep file IDs, email and account details private; provide a redacted transcript for diagnosis. Verify unchanged existing-installation recall separately without resetting it. Do not declare a pass from the final natural-language claim alone: check actual connector results. Failure or inability to expose these results stays unverified.
