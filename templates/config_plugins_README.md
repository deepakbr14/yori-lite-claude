# Plugin configuration in Google Drive

This visible My Drive folder contains configuration pointers for plugins. This is a proposed convention, not a Google or Anthropic standard. Each user owns their own folder. Do not share it by default. Google permissions determine who can read it.

Yori Lite uses `yori_2d970fa0-89e4-451e-802b-9f836f99d9e1.json` and published plugin UUID `2d970fa0-89e4-451e-802b-9f836f99d9e1`. The UUID is identical for every installation, not a user ID. Its schema_version 1 configuration selects exactly one authorized Cortex folder. The label does not prove permissions. Never store passwords, tokens or secrets here. Other plugins may keep their own files; do not overwrite them.

Duplicate folders/files must be resolved explicitly. Resolve the exact root parent, owner, filename, plugin_id and folder IDs; do not pick a fuzzy match. New chats must rediscover and verify this pointer. A naming convention does not make a plugin always run. Unsupported schemas fail visibly; future migrations need an explicit versioned process and must preserve the original selection.
