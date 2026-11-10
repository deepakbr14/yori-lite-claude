# Readable README installation and repair

READMEs are an intentional exception to metadata memory: their instructions live in ordinary file BODY content. Editable memory and configuration stay in descriptions. Do not require editing any existing file contents, a new connector, Apps Script or a Cortex rebuild.

## New setup

In the selected Cortex root, create a text/plain UTF-8 file named `README - About this Cortex.txt` with the complete contents of templates/cortex_README.txt as its actual body. In the user's config_plugins folder, when registry instructions are missing, create `README - Plugin settings.txt` with templates/config_plugins_README.md as its actual text body. Normal file creation with initial content through the existing Drive connector is sufficient; do not assume a separate Docs editing capability.

A short optional metadata description can identify role: `record_type: human_readme; role: cortex_guide` or `role: config_guide`; it must not be the sole location of the instructions. Add `guide_version: 0.2.1` and a stable per-attempt operation_id for timeout recovery if the tool supports setting description. If not, verify candidate IDs/bodies directly. No change to the config schema or memory descriptions.

For each new guide, verify the returned parent/ID and read the actual BODY back through the connector. Compare it with the intended text. A metadata description read-back does not verify a readable README. If the tool cannot create or read body content, leave memory setup intact, report the guide limitation briefly, and do not claim this repair passed. Do not create an empty substitute. Never change permissions to make a guide visible.

## Existing initialized Cortex

Use the already-resolved exact Cortex/config IDs. Never recreate Self/People/Knowledge/History, rerun first-use initialization, replace the config, or change the active pointer to repair a README. Reuse the normal scoped root listing to identify candidates during the first 0.2.1 activation or explicit guide repair; no additional full-Drive searches and no repeated check per skill/turn. A marked existing guide or known readable README needs no update solely because the plugin version changed.

- Existing nonempty readable README body: preserve it byte-for-byte, even if user-customized. Do not overwrite with a template.
- Legacy README with instructions only in description and an empty body: preserve that file and metadata. Create the distinct body-filled guide name above in the same parent, referencing the old file ID in the new guide's optional metadata. Do not copy unrelated private data into a broader folder.
- Missing README: create the appropriate body-filled guide only, without reinitializing anything else.
- Existing new-named candidate with empty body: do not overwrite or create another same-named guide blindly. Explain the incomplete repair and ask for resolution if it cannot be safely distinguished from an in-flight operation.
- Multiple/ambiguous candidates or a creation timeout: re-list within the same exact parent and inspect operation_id/role and actual body before retrying. Reuse a verified successful result. If uncertainty remains, stop the repair; do not create duplicates or delete any candidate. Concurrent creators can still race because Drive names are not unique. Detect duplicate outcomes and report them, not pretend a transaction existed.

Verify the actual body when assessing an unverified/legacy candidate. Once a guide is verified in this chat, retain its ID/outcome in turn context and do not reread it for every learning turn. Future chats can reuse a marked guide from their ordinary listing without reapplying migration. A user-reported blank/deleted guide invalidates that assumption and triggers repair verification.

README maintenance is not memory learning: exclude human_readme documents from topic searches and do not create History contributions for routine guide installation. Unsuccessful guide repair must not block otherwise authorized learning or prompt recreation of the Cortex.
