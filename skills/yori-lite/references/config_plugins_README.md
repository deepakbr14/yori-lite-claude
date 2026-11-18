config_plugins
A shared place for plugin settings

A proposed open convention

Plugins often need to remember where a person's files live. This visible folder gives them a small, predictable place to keep those pointers, so users do not have to repeat setup in every new conversation.

This is a proposed open convention, not an official Google, Claude, or ChatGPT standard. Developers may adopt it wherever their host can safely find, read and write Google Drive files. A common format does not prove that every platform supports those operations.

One folder for a person. One configuration for a plugin.

Each person has their own config_plugins folder directly in their Google My Drive. Different plugins can share this directory while keeping separate configuration files. Actual notes, projects and other working data stay in the storage folders chosen by that person.

A publisher chooses one permanent random UUID for a plugin. The same UUID ships with every installation and every routine update. It identifies the plugin—not a user, company, device or storage folder. Using a fixed UUID keeps discovery stable when the display name changes and helps unrelated plugins avoid claiming each other's settings.

Name the configuration file with a readable prefix and that UUID:

    <plugin-prefix>_<fixed-plugin-uuid>.json

Keep an established filename unchanged. Do not generate a new plugin UUID on each install, and do not rename somebody else's configuration.

Two independent plugins, side by side

    My Drive
      config_plugins
        atlas_83db4aa0-8725-49bc-9422-0ea47df9620e.json
        planner_41a15317-a310-4f31-93ad-3b661e40e3cd.json

Atlas could point to this user's research folder. Planner could point to that user's planning folder. Another person has their own config files; their Atlas may point to a different research folder, or to the same shared folder when they deliberately choose to collaborate. Sharing the directory convention does not share the plugins' data.

These UUIDs are examples for two unrelated plugins, not the IDs to copy into a new product. Each publisher generates and publishes their own UUID once.

What goes in a configuration

Keep a format version, the fixed plugin identity, and the exact Google Drive IDs of the user's selected storage folders. A friendly label helps the person recognize a folder; the ID is what the plugin uses. A plugin may support one folder or several, according to its own documented format. This convention does not require existing plugins to add multiple-folder support.

Publish your plugin's small configuration format and how it stores it. Ordinary JSON file contents are one option. A connector that can edit descriptions but not existing file contents can store the JSON in the description instead. Read the field your plugin documents; never silently choose between conflicting copies. This README itself always has readable file contents.

Discover, verify, reuse

Find the intended connected Google account and its own My Drive root. Find exactly one config_plugins folder there, then the plugin's exact configuration filename. Inspect ownership and parent location—not just a name from search. Follow all result pages, validate the format version and plugin identity, then verify permission to use the saved folder IDs.

Once resolved, use exact file IDs during the conversation. Rediscover in a new conversation rather than pretending chat history is durable settings. Reuse verified results within a turn; do not repeatedly search for the same file.

If nothing exists, guide the person through normal setup. Ask them to choose their storage and explain who can see what is saved there. Create only your plugin's configuration and verify it was saved. Leave unrelated plugins' files and the shared README alone unless an authorized maintenance process explicitly covers them.

When something is unclear

Google Drive permits duplicate names. If two matching configuration folders or files exist, stop and ask for resolution; do not select a random result or create a third copy. If a file is invalid, its format version is unsupported, or its saved folder is inaccessible, explain the specific problem. Never fall back to another person's data or a different folder without an explicit choice.

Permissions come from Google Drive, not the configuration. A label such as “private” or “team” grants no access. Verify the account and file access used for each operation. Keep tokens, passwords and private keys out of this visible directory. Do not make the registry public.

For developers adopting the convention

Publish your fixed UUID, filename, format and storage field. Test first-time setup, fresh-session discovery, missing access, duplicate files and concurrent edits in the host your users actually use. Change formats through explicit, compatible migrations; a version bump alone must not reset storage.

Claude and ChatGPT plugins could use the same directory convention when their respective connectors support it. Test each independently. Adoption is voluntary, and this proposal makes no claim of official approval or universal compatibility.
