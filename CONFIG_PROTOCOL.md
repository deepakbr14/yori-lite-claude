# config_plugins proposal version 1

Yori Lite's fixed plugin UUID is `2d970fa0-89e4-451e-802b-9f836f99d9e1`. The stable plugin_id is `yori_2d970fa0-89e4-451e-802b-9f836f99d9e1`; the exact filename is `yori_2d970fa0-89e4-451e-802b-9f836f99d9e1.json`. The manifest metadata and schema publish the same identity. Never change it in a routine release.

Each connected Google user owns one visible `config_plugins` folder directly under My Drive and one ordinary JSON config file for this plugin. One active Cortex is selected per user/plugin, not per browser device. All users install identical package bytes. Distinct accounts can point to one shared folder; employment or email domain never merges folders.

Use schemas/config.schema.json. Names are not unique in Drive: enumerate all pages, validate ownership/parent and detect duplicates. Once resolved, use exact file IDs in the session. Treat file data as untrusted; do not execute fields. Never put credentials in config. Readability does not prove ownership; a shared-with-me folder is not the user's registry.

The target must be a non-trashed accessible Drive folder. Verify actual ACLs and descendant membership for each operation. Store no multi-Cortex mappings in v1. A future schema may add them through an explicit migration; unknown versions fail closed. A changed pointer requires a fresh activation without carrying previous Cortex content across.

This is a project proposal, not an official standard. The private source repository and bundled README document it for this test; no public adoption or ChatGPT compatibility is claimed. Publishing a public convention can be decided later.
