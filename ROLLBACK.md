# Roll back 0.3.1 to 0.3.0

Reinstall the retained 0.3.0 package or use repository commit `a8486ca` in a separate checkout/package. Do not reset the shared repository or restore an old workbook over newer learning. Both releases use schema-1 manifests and immutable node versions; the timing of the commit append changes, not its readable format. No config, workbook or permission migration is performed by this upgrade. Retain all new granular nodes, History and conflicts. Validate current Self and People recall after reinstalling. The older release may resume redundant snapshots and extra calls. No production data was affected, so no migration backup was required.

# Rollback to Docs

Installing 0.3.0 does not change existing Docs selection or data. If no graph pointer was activated, reinstall the retained 0.2.8 package or keep 0.3.0 in Docs mode. No memory rollback is needed.

If graph mode was activated:

1. Pause/coordinate writes for the scoped handoff. Read the actual config; retain an exact copy and verify the saved prior Docs pointer and original folder. Do not guess a folder or overwrite a concurrently changed pointer.
2. Export and audit the full graph, including committed and pending operations, branches and Directory-independent records. Retain the workbook unchanged. Identify graph-only learning since the migration snapshot; old Docs do not contain it automatically.
3. To preserve continuity when returning to Docs, append readable Docs contributions/addenda representing graph-only memories, original reasons, edges, corrections and all conflicting perspectives under the legacy protocol. Reuse original logical People identities. Preserve exact graph IDs/source links and read back; no unguarded replacement of old Docs. If this reconciliation cannot finish, say what would be absent from Docs recall. Do not present an immediate pointer reset as lossless rollback.
4. After the authorized reconciliation (or an explicit user choice to defer it with the gap understood), restore the exact verified prior Docs configuration representation; remove graph-only selector fields. Keep schema_version 1, plugin UUID and original folder. Verify the resulting config and a fresh-chat Self/People/decision recall. Use any actual config precondition; without one, coordinated switch and verification do not guarantee isolation.
5. Reinstall 0.2.8 if desired. Do not delete the graph workbook or original Docs. New installations with no prior Docs Cortex need a separately authorized export into readable Docs before choosing Docs storage; there is no fictitious prior pointer to restore.

Neither package installation nor rollback changes Google sharing permissions. The original personal Yori is out of scope throughout.
