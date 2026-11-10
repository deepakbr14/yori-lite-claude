# Updating to 0.2.2

No configuration, identity or memory-format migration. Same fixed UUID, schema, file IDs and selected Cortex. Internal skill names remain compatible; yori-lite is the public entry point. The registry README becomes developer-facing body text. Only an exact, unchanged, identifiable setup-generated Cortex guide may be recoverably trashed under README_MIGRATION.md; user-authored/customized files remain. No Cortex reinitialization.

## Historical 0.2.1 behavior (superseded for README maintenance)

The selected Cortex, configuration schema/UUID, memory format, Self and History are unchanged. 0.2.1 added a human-readable Cortex guide. In 0.2.2, follow [README maintenance](README_MIGRATION.md) instead: registry-only documentation and narrowly verified Cortex-guide retirement. Installation alone does not operate on Drive. No reinitialization or setup probe is needed for an initialized Cortex.

## Older 0.1 compatibility

Plugin name yori-lite, marketplace yori-lite-claude, fixed plugin UUID, configuration filename and schema_version 1 are unchanged. Updating the plugin does not modify any Drive files by itself. No production data migration is performed by this release.

Existing config stored in file contents remains readable when description is absent/empty. New config uses description. No existing file-content edit is required. If nonempty metadata config is malformed or two representations disagree, ask for repair; no silent fallback or switching.

Do not treat old content-based Self/People/Knowledge/History files as empty when their descriptions are blank. Read their in-scope contents when relevant and label the format accurately. Do not automatically overwrite or retire them.

If the user explicitly requests conversion of a selected legacy memory, read its complete original content, preserve its existing file ID/source, create and verify new metadata memory descriptions in appropriately sized pieces, and record provenance. Leave originals intact and record which IDs now represent the converted memory. Reconcile rather than duplicate claims on later recall. No bulk conversion, deletion or folder migration is part of normal startup.

New learning uses metadata descriptions. Guarded revisions operate only on verified metadata memories. Existing body-based originals remain readable evidence until deliberately converted. A fresh disposable Cortex is the simplest way to test 0.2 without changing an old Cortex.
