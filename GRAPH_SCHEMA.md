# Sheets graph schema 1

One workbook per Cortex. Five tabs, with row 1 headers in exactly the order below. Complete memory prose is stored in Nodes.content, not in a linked Doc. Types and column order are also in schemas/graph.schema.json. Empty optional values are empty strings; unknown event dates stay unknown. No formula cells in storage.

| Tab | Columns, in order |
|---|---|
| Nodes | node_id, revision_id, operation_id, kind, title, content, subject, contributor, attribution, source, created_at, updated_at, event_time, base_revision_ids, version, status |
| Edges | edge_id, revision_id, operation_id, from_node_id, to_node_id, relation, strength, evidence, contributor, attribution, created_at, base_revision_ids, version, status |
| History | event_id, operation_id, event_type, entity_id, content, contributor, attribution, source, recorded_at, base_revision_ids, manifest |
| Directory | hint_id, node_id, revision_id, row_number, operation_id, verified_at |
| Metadata | record_id, key, value, recorded_at |

Nodes include Self, People, Knowledge, Concept and other meaningful categories. `node_id` is permanent across versions; migrated source IDs are retained where possible. `revision_id` identifies one full immutable version. Rows are never overwritten to make them current. `base_revision_ids` is a JSON array of predecessor revision IDs; current heads are derived from valid committed ancestry. `version` is a positive integer for display only. Two competing heads do not become one because their version numbers or timestamps differ.

Edges reference permanent node IDs and contain a specific supported relation, evidence, contributor and attribution. Strength is an optional textual qualifier or exact decimal text, not an invented similarity score. Edge revision ancestry works like node ancestry. Status is `active` or `retired`; retirement is a new version. No hard deletion or implicit transitive links.

Attribution values: `explicit_statement`, `external_evidence`, `inference`, `decision`, `mixed`, `unknown`. Complete content/evidence carries claim-level authorship, uncertainty and original reasons. For `mixed`, attribute individual claims in readable prose. A People record can contain the existing Recognition section; shared Google access does not authenticate the speaker.

History event types include contribution, prior_state, correction, migration_evidence, legacy_history and commit. Prior-state content preserves the entire meaningful previous version; the utility uses canonical row JSON for exact snapshots. A commit's manifest references every authoritative payload row by tab and its row ID (revision_id for Nodes/Edges, event_id for History). It contains either SHA-256 of canonical full row JSON or the exact full row payload. Commit events do not include themselves in their manifest. Verify manifest members before accepting current memory. The full procedure is in references/graph-cortex.md.

Canonical row hashing in the supplied utility is UTF-8 JSON with sorted keys, no extra separators/spaces, Unicode preserved, and all schema keys present. Version and row_number are integers; semantic fields, timestamps, strength and embedded JSON columns are strings. Use the same trusted implementation or exact-payload verification; never guess a digest or silently normalize meaningful whitespace. A repeated row ID with different content is an integrity failure, even if the difference looks technical.

Directory rows are optional immutable hints, not the truth about current state. `row_number` is a 1-based physical sheet row >=2. Verify node_id AND revision_id after direct lookup, then check complete committed heads. A stale or missing hint falls back to scoped ID lookup and can be superseded by a new hint. No sorting/inserting/deleting storage rows in the application protocol.

Metadata bootstrap keys: cortex_id (generated UUID), schema_version (`1`), storage_format (`sheets-graph-v1`) and created_at (reliable time or unknown). Synthetic workbooks also have fixture=`synthetic only`. Migration may add source folder, snapshot digest and staged status. Metadata rows are appended; conflicting settings require explicit correction evidence rather than arbitrary latest-row selection. The config's workbook ID plus verified folder ancestry is the scope boundary; a copied metadata value cannot authorize another workbook.

For a real new installation, initialize only meaningful starting Self from templates/initial-self.md (omit its legacy format footer; represent kind/version in columns). Never copy the synthetic amber/person/decision fixture into a real user's identity. Verify headers, Metadata, initial Self, contribution and commit before writing the graph config pointer. No Cortex README or permanent probe is needed.
