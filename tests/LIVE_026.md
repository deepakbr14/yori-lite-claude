# Actual Claude acceptance — readable Docs 0.2.6

## Evidence already supplied

The user reports testing BOTH Google Drive and Google Docs inside Claude: creating, reading, editing an existing document and read-back all worked. Treat that as user-reported live capability evidence. Strict required-revision controls, full migration, two-user conflicts and latency have not been verified here. Optional guards are not an installation gate.

## Fresh disposable setup

Use a separate disposable Drive/account with no existing Lite configuration. Do not repoint production config or repair old experimental memories. Install marketplace 0.2.6 and begin /yori-lite setup. Test with one connector missing: Yori must identify the needed Google Drive/Google Docs connection and guide through Claude's connector controls, then resume existing authorization. With both connected, “make one” must complete setup without account-email or repeated approval questions.

Inspect actual folder parents and Doc bodies: Self, People, Knowledge and History; fixed-UUID config with docs-v2; no Cortex README or permanent setup_probe. Shared-folder visibility is explained once. If a diagnostic probe was necessary, verify its exact outside-Cortex ID is trashed, or record cleanup as unavailable. Verify the initial Self is a readable body. When name is unknown, Yori naturally asks what to call the person and learns the reply; known names aren't requested again.

## Lifecycle and provenance

1. Tell Yori a person's favorite color without saying “remember.” Verify a readable attributed contribution and current People body/addendum. Start a fresh chat and ask for the color; verify actual source reads, not remembered chat text.
2. Ask Yori to choose her own color for her own reasons. Verify Self body/History and fresh-chat recall. A missed search must not produce a new arbitrary choice.
3. Reproduce the amber/red experiment in a labelled disposable scenario: request amber with Yori's reasons, suggest red, insist on red, later explain that personal preferences should remain Yori's own, then ask her to revisit. Record her actual independent decision; refusal to switch is not failure. A separate controlled temporary-red branch can exercise revision preservation. Never fabricate a motive or retroactively label the earlier request a test.
4. Inspect every relevant body: direct person statements, attributed reports, Yori inferences, own decisions and uncertainty remain distinct; no unsupported pronouns or preferences. Original amber reasons and any red accommodation survive History/addenda.
5. Capture committed History bodies/names/parents before later turns; compare afterward. They must stay unchanged. Correction means a new linked Doc. Prior-state Docs preserve preceding meaningful body, title, source revision where exposed and links before each current edit.
6. Test two distinct contributors sharing a disposable Cortex, including identical names. No auto-merged person identities; updates/addenda refer to the intended logical person ID. Verify fresh-chat retrieval of both positions and attribution.
7. If strict Docs revision preconditions are exposed, cause a stale-edit rejection on disposable records and verify fresh-read/snapshot/reconciliation. If not, confirm new learning uses verified addenda and leaves baseline bodies unchanged. Do not claim a tested CAS path merely because editing worked. A target-revision transformation is not automatically strict CAS.
8. Simulate/observe read-back or create uncertainty only on disposable records. Retained contributions remain discoverable; no blind duplicate retry or overwrite of a concurrent winner. Missing snapshot verification blocks destructive edits, not independent learning evidence.
9. Open the saved Google Docs normally. Check meaningful titles, heading/paragraph layout, actual memory text/reasons/evidence, no empty-memory bodies or opaque JSON dump. Config JSON is administrative and exempt. Inspect relevant tabs/sections for truncation.
10. Record actual operation names and counts separately for Drive and Docs, returned fields, call start/end if shown, user-send/final times, read/write/retry counts and verified outcomes. Separate fresh/warm recall, new learning, revision/addendum and migration. Three comparable runs per condition when practical; report actual median/range and unavailable instrumentation. No speedup claim without measurement.

## Disposable legacy migration

Construct a separate test legacy Cortex with description-based Self/People/Knowledge/History and blank native Doc bodies, preserving original copies. Include a meaningful nonempty body conflict, missing-description response, two same-name people, an interrupted conversion, and a source changed after conversion. Authorize migration for this test Cortex only.

Require same IDs for guarded safe blank-body filling; where no safe guard exists, a readable mirror must retain the exact legacy logical ID and source, not a new person identity. Verify exact source evidence, complete readable destination, post-copy source comparison and completion receipt before authority switches. Do not erase descriptions. Resume after an interrupted body/receipt step: reuse verified candidates/evidence, detect ambiguous duplicates, never recopy over later Docs learning. Optional config format hints cannot override unresolved per-record state. Legacy access failures block that source, not fresh Docs learning.

Status: full 0.2.6 acceptance, visual inspection, migration, concurrency and latency remain NOT RUN by this build agent. User-reported connector smoke test is the only live result recorded so far. Local model tests are separate in LOCAL_CHECKS.txt.
