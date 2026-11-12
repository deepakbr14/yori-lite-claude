# Configuration protocol

Fixed plugin UUID: `2d970fa0-89e4-451e-802b-9f836f99d9e1`.
Exact plugin_id and file basename: `yori_2d970fa0-89e4-451e-802b-9f836f99d9e1`.
Exact filename: `yori_2d970fa0-89e4-451e-802b-9f836f99d9e1.json`.

Each connected Google user has one owned `config_plugins` directly under My Drive. One plugin-specific configuration selects one Cortex. The plugin UUID, filename and schema_version 1 remain unchanged in 0.2.0. One Cortex is effectively per connected Google user/plugin, not per browser device; all people selecting the same folder join one Yori. Multiple named Cortexes and switching are not implemented.

New files store JSON conforming to schemas/config.schema.json in description, with empty contents. Nonempty malformed description is an error, not an excuse to use old contents. For 0.1 compatibility only, absent/empty description permits reading legacy JSON contents. If both representations exist and disagree about the target, stop for repair. Do not automatically rewrite or bulk migrate configuration. No credentials belong here.

Resolve unique owner/root-parent/name with pagination, then operate by exact IDs. Duplicate names are legal in Drive; config requires deliberate disambiguation rather than random choice. Validate actual target permissions and parent ancestry. This proposed convention is not an always-on startup hook or cross-platform guarantee.

## graph extension (0.3.0)

All discovery, naming, schema_version 1, ownership, permissions, description/body precedence and selected folder behavior above remain. `storage_format: sheets-graph-v1` adds `cortex_schema_version: 1` and `active_cortex.google_sheets_spreadsheet_id`. The folder stays the permission/scope boundary; do not replace it with a workbook URL. Verify native workbook ID/parent and graph headers before saving the pointer. Absence of graph fields never implies an empty graph. Existing configs without these fields remain valid. Do not store auth credentials or reset participant mappings.

Installation does not switch an existing config. Migration stages a workbook in the same selected folder, preserves an exact local/administrative copy of the old config representation, and requires a source/destination audit before a separately authorized pointer switch. No new config_plugins convention, plugin UUID or automatic folder switch. Rollback restores the verified old config after preserving graph-only learning; see ROLLBACK.md.
