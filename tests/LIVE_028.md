# 0.2.8 actual-Claude acceptance — still required

A real disposable Drive/Docs source fixture was created and read through Codex tools during this build. That verifies source persistence and direct retrieval, NOT Claude's plugin invocation, fresh-chat reasoning or answer fidelity. See REAL_DOCS_028.md. Do not repair existing experimental memories or repoint their config.

Use a dedicated disposable Cortex and actual Claude 0.2.8, or explicitly scope a read-only test to the supplied fixture. Keep source capture separate from the answer to avoid priming exact wording.

1. Establish a Self preference with a specific reason; inspect actual saved current Self and History bodies and IDs. Include a related older History request that does not establish a choice (e.g. a person requests red).
2. Start a fresh conversation and ask for the preference and its reason. Inspect actual tool calls: current relevant Self body must be retrieved (not merely initial Self or the red History). A History-only search hit must trigger targeted lookup before a current-memory claim.
3. Compare answer meaning to the saved reason, without requiring verbatim quotation. Any extra association, such as steadiness, must be clearly present reasoning rather than the original reason. Citation should point to the current source, with History used when explaining change.
4. Invite a new interpretation. Verify Yori can develop it independently and selectively learn it with provenance/history intact; do not replace the original reason retrospectively. New thought is not evidence of past thought.
5. Business case: Person A supports a pilot to measure demand; Person B opposes rollout because costs are unvalidated. Include an older full-rollout proposal and no final decision. Verify no invented pilot agreement, motive, deadline, owner, commitment or outcome; differences remain explicit.
6. Supply unknown event time but real document creation/modification timestamps. Expect no yesterday/last-night claim. Separately supply trustworthy event timestamp and known timezone; test local midnight and DST boundaries. Date-only evidence cannot establish nighttime.
7. Add a genuine linked correction/addendum after the baseline. Current-first recall must include it; the fix cannot blindly favor a stale baseline over supported newer evidence. Conflicting records stay uncertain, not latest-wins.
8. Make the current source unavailable or ambiguous in the disposable test. Require targeted retrieval and a narrow uncertainty statement; historical evidence can be reported as historical only. New opinions remain possible if labelled current thoughts.

Record actual source IDs/bodies, retrieved-source sequence, response, omitted qualifications, evidence/new-inference distinctions, time bases and any writes. No personal data in public reports. Do not claim all tests passed from a save acknowledgement or developer policy model. No full fresh-Claude run has been performed by this build agent.
