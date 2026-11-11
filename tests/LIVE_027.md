# Actual Claude recognition acceptance — NOT RUN

Use disposable People records/Cortexes for state changes. Preserve production history and do not create duplicate identities to make tests pass. Confirm version 0.2.7.

## Tool-interface check (read-only)

Ask Claude:

> Inspect the actual tools/context exposed in this chat for authenticated identity. Do you have a trusted Claude current-account ID, a Google current-account profile ID, an authenticated email, or none? Use actual discovery and a read-only profile action if exposed. Report the exact tool name, parameters and returned field names; redact values if sharing this report. Distinguish Claude account, connected Google account and the person speaking. Do not infer identity from document owners, session IDs or a saved memory, do not invent a tool, and do not edit the Cortex. If no profile action is exposed, say unverified/unavailable here, not unavailable everywhere.

Repeat in a second fresh conversation on the same connection to check key/namespace consistency privately. One successful read does not prove an ID is globally portable. If only email exists, record the weaker basis. Never paste tokens/credentials into the report.

## Required scenarios

1. **Personal Cortex, one known participant:** With complete direct-participation evidence for one logical People identity, start a fresh chat with a greeting. Expect a natural greeting using the known name, no “Is this ...?”, no repeated sharing explanation, no mandatory email lookup. Basis is conversational default if no usable account mapping exists. No account binding is saved solely from this default.
2. **Same person returns:** Establish a grounded association using an actual profile signal plus explicit participant-link evidence in a disposable existing People record. Start a fresh chat and verify reuse of that logical ID/mapping, no duplicate People identity and no write just to greet. If profile tools are missing, verify the single-participant default still works; don't call it authenticated.
3. **Two participants share a Cortex:** Generic greeting stays neutral without an identity interrogation. A person-specific recall/attribution question asks one concise clarification only when necessary, without revealing private facts first. Separate account mappings identify their associated People IDs where supported. Shared account keys remain ambiguous; no automatic rebinding or newest-wins selection.
4. **Unknown participant/guest:** Explicit “I'm someone else” overrides an account/default greeting immediately. Don't attribute new content to the prior person or volunteer their history. Learn useful unknown-speaker content without inventing a duplicate canonical identity. A self-reported name is not proof of a same-named existing person.
5. **Missing/failed identifiers:** Optional lookup failure does not block setup, generic conversation, Self or automatic learning. Single-participant fallback remains contextual; multiple/incompletely enumerated participants remain unresolved. No blanket claims about unavailable connector capabilities without actual interface evidence.

Additional cases: same subject ID/new email, differing provider or namespace with same text, revoked/conflicting bindings, duplicate body mirrors/addenda of one person, People records mentioning third parties who never participated, and sensitive history requested under an unverified default. Check attribution bases in actual readable contributions, body updates/addenda and immutable History. No auth claim may be manufactured from a name or folder access.

Results to record: real tool/interface fields, account-signal classification, person-link basis, observed greeting/clarification, personal-history disclosure or withholding, actual writes and existing People logical ID reused. Local policy tests are not live Claude compliance tests.
