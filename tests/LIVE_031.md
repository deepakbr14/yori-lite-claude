# Claude acceptance prompt — 0.3.1

Run in Claude with Yori Lite 0.3.1, connected Drive and Sheets. Use a new named disposable Cortex; never switch or edit the real config pointer. Start a separate fresh conversation for recall, explicitly supplying only its test workbook ID. Do not copy prior answers into that chat.

Paste:

> Test Yori Lite 0.3.1 only in a new disposable workbook named DISPOSABLE Yori 031 acceptance. Preserve production config and all existing Cortexes. Inspect the actual exposed tools: record exact operation names and whether they expose atomic multi-tab genuine append and grouped reads. Do not substitute Google API documentation for connector capability. If atomicity is undocumented, use a disposable invalid-last-subrequest batch and verify earlier rows were not appended; otherwise retain the staged fallback. Record authorization delays separately where visible, without bypassing approval.
>
> Create synthetic participant Alex and then learn “my favorite number is 5” with explicit attribution. Use a small preference node and evidence-grounded about edge; leave Alex's profile unchanged. Capture all connector/host calls and timestamps if visible. Repeat three independent small-fact saves. Correct the preference to 7, preserving its exact prior immutable version and reason. Verify exact payloads and commit, immutable History, stable IDs, no routine Directory write, and no redundant full-profile snapshot. Test one-hop preference-to-person retrieval with commit/current-head checks.
>
> Simulate an uncertain acknowledgment after a successful append: reconcile the original operation IDs from storage and do not blindly append again. Distinguish simulation from a real network failure. For concurrency, coordinate two authorized test sessions that read the same base and submit different corrections; preserve both branches and attribution. If two users are unavailable, label sequential stale-writer simulation honestly. Never silently resolve disagreement by timestamp.
>
> Report per scenario: write calls, read/verification calls, other calls, total response time, model preparation and authorization time where observable (otherwise unknown), exact integrity assertions and any fallback. A missing verification ID must trigger lookup, not a fabricated pass or a forced two-call limit. Compare first-chat versus later-turn costs. Preserve learning frequency and supported edges.

Fresh-chat prompt:

> Use only the disposable test workbook [ID], without changing my saved Cortex selection. Retrieve current Self and Alex's preference with supporting current node IDs and relevant History. Identify competing branches instead of choosing a last-writer winner. Explain the original reason faithfully and distinguish any new interpretation. Report actual tools and source IDs used. Do not treat this request as authorization to edit the real Cortex.

Acceptance is two Sheets calls for an ordinary already-scoped save **when the connector supports the safe fast path**; extra bootstrap/preparation/recovery calls must be counted, not hidden. Capture full elapsed response time externally if Claude cannot observe it. Retain the disposable workbook for audit; do not repair the test data to make assertions pass.
