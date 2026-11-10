# Registry README and safe Cortex-guide retirement — 0.2.2

The only new README belongs in the user's config_plugins directory. The Cortex holds Self and developing memory, not installation instructions. Never create another Cortex README. Configuration filenames, UUID, schema, pointers and memory descriptions are unchanged.

## Registry guide: readable and vendor-neutral

Use templates/config_plugins_README.md as the actual UTF-8 text/plain BODY of `README - Plugin configuration.txt`. Its section spacing is readable in an ordinary Drive text preview. Description may carry `record_type: human_readme; role: config_guide; guide_version: 0.2.2; operation_id: <stable token>`, not the instructions themselves. Do not require content editing or a separate Docs connector.

Create and read back the complete body and verified parent. If creation/body reading is unavailable, report that maintenance limitation; do not create an empty substitute or block otherwise working memory. No screenshot or rendered-in-Drive verification is claimed until actually observed.

On existing installations, reuse a verified matching guide with the complete current body. If only the known earlier Yori-generated registry guide exists, create this distinct new filename and preserve the old file; existing contents cannot be edited through the tested connector. If an existing guide is customized/user-authored, do not overwrite, rename, or delete it. A new separately titled convention guide may coexist, but never replace someone else's README. Conflicting new-name candidates stop maintenance for resolution. No config file is renamed. Do not change other plugins' settings.

A timeout is not evidence of failure: re-list the exact parent and compare operation_id, role and full body before retrying. Reuse a verified completed result. Multiple identical guides can be a race; do not silently pick one for destructive cleanup. Maintain once at relevant activation, not every learning turn.

## Remove ONLY a known generated Cortex guide

The user authorized removing the old setup-generated Cortex README. Prefer reversible Trash, NEVER permanent delete. This narrow exception does not authorize deleting memory, Self, History, user-authored documents or the Cortex folder.

Require ALL of the following before trashing:

1. Exact current parent is the selected Cortex root, not config_plugins or another Cortex; non-trashed file ID has been inspected.
2. Exact expected name is `README - About this Cortex.txt`.
3. Verified setup provenance: an actual creation receipt for this file ID from prior setup, or the expected generated marker `record_type: human_readme`, `role: cortex_guide`, `guide_version: 0.2.1`. A name alone, filename similarity, or an email guessed as creator is not provenance.
4. Full actual BODY exactly equals the frozen references/legacy/cortex-readme-0.2.1.txt template. Optional SHA-256 in guide-identities.json is supporting evidence; do not invent a hash check without a tool. Added/changed/removed text, extra meaningful metadata, uncertainty about provenance, or an empty-body/custom README means leave it untouched. Inspect metadata too: preserve anything carrying user content rather than just setup markers/operation ID.
5. Read fresh etag and parents; recheck expected parent immediately before trash. Use actual connector-supported expected-etag guarding on the trash metadata update. On conflict, stop cleanup or reread and revalidate ALL conditions, never simply retry against a new etag. If guarded trash is not exposed, leave the guide and briefly explain when relevant. Do not substitute unguarded deletion.
6. Read back `trashed=true` for that same ID. Unknown outcome is reported as unverified; no repeated destructive retries. An unexpected move stops cleanup; a move does not change etag, so this is not a transaction and external-move races remain a limitation.

For unmarked guides with no creation receipt, unknown/custom versions, same-name duplicates, or differing contents: leave them. Ask the user to identify a file only if they want that ambiguity resolved. Never infer it is safe to trash from the word README. Never reset or recreate the Cortex.

Frozen legacy files ship only as comparison evidence for this cleanup; they must NEVER be installed as new Cortex guides. Once no eligible candidate remains, there is no cleanup on ordinary turns. Reuse scoped activation listings and same-turn results; no new global scan or memory event for documentation maintenance.
