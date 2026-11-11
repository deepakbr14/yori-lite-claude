# Self continuity investigation — before implementation

## Confirmed

The user reports that Lite recalled their number/color/name but chose 6 instead of recalling Yori's earlier favorite number. The earlier number and original save receipt have not been provided. This is a user-reported incident, not a reproduced run.

Source inspection of 0.2.4 found that the main Skill already required Self recall before answering with an existing Cortex, and the recall Skill required initial/current Self plus relevant History. Thus Self was intended to load at fresh-chat startup, not only on explicit request. Actual execution is unknown. Self changes were first-class learning candidates, but no explicit distinction prevented incomplete recall from becoming a new preference. Yori-authored choices were not clearly singled out from general learning candidates.

Read-only Codex Drive discovery located a Lite config file under an owned root config_plugins folder. A metadata request explicitly asking for description did not return that field; a default metadata request also omitted it. Fetch returned an empty body. These observations do NOT establish an empty description, missing pointer or missing memory. Without the selected Cortex pointer, the investigation did not guess a Cortex by name, inspect personal Yori, or write any Drive data. No private file IDs, emails or memory contents are included here.

## Unresolved incident questions

- Original choice saved? Unknown; needs original contribution/receipt or current/historical description evidence.
- Saved but missed? Possible; initial Self alone, bounded retrieval, unindexed description search, pending contributions or failed Skill activation could explain it. None is confirmed.
- Not saved? Possible; a Yori-authored choice may have been treated as transient conversation, or a write/verification may have failed. Neither is confirmed.
- Overwritten, superseded or obscured? Unknown; compare Self descriptions, immutable contribution/prior-revision records, target IDs, operation IDs and any actual write trace. An old snapshot does not prove its successor committed; modification time alone does not prove deliberate revision. Drive file-content revisions may not expose description history.
- Other Self memories affected? The instruction gap is general and could affect preferences/goals/judgments, but no other incident is established.

Root cause of this specific incident is NOT yet established. The smallest justified change addresses the confirmed instruction gaps without restoring an invented old favorite, erasing 6, or altering production records. Read-only incident audit and actual Claude acceptance remain required; see LIVE_025.md.
