# <topic>

schema_version: 1
operation_id: <unique token reused for retries>
event_type: <contribution/correction/retraction/disagreement/self_revision/organization>
status: <reported/supported/disputed/historical/retracted/inferred>
contributor: <confirmed alias or unknown>
identity_basis: <connector_account/user_confirmed_alias/unknown>
observed_at: <known timestamp or unknown>
time_basis: <host/tool_createdTime/user_reported/unknown>
effective_at: <only if supplied; otherwise unknown>
source_kind: <current_conversation/in_scope_document>
source_url: <verified URL if available; otherwise unavailable>

## Statement and supplied reasons

<Faithful concise statement. Reasons only if supplied.>

## Evidence and interpretation

<Relevant short source excerpt or faithful paraphrase; distinguish inference.>
Confidence and basis: <assessment grounded in evidence>
Related event/file IDs: <verified IDs or none>
Prior claims affected: <verified references or none>
Unresolved: <what remains uncertain and what would resolve it>

The connector-returned Drive file ID is the canonical record identifier. Verify this operation_id and full content after creation.
