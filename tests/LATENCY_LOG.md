# Live latency observation

Record disposable runs only; no production data. Separate setup/fresh-chat recall from warm learning and corrections. No fabricated per-tool timings when the client does not expose them.

| Version | Client | Scenario / fresh or warm | User sent | Final reply | Observed elapsed | Connector calls | Retries | Learning/history/read-back verified |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.2.0 | user-reported | fictional spaceship Aurora learning | unavailable | unavailable | approximately 35 seconds | unknown | unknown | first learning reported successful |
| 0.2.1 | | | | | NOT MEASURED | | | |

If tools expose durations, record operation name and start/end, grouping actual parallel calls. Otherwise record only total wall time and visible call count. Compare equivalent dummy tasks and at least three runs where practical; report range/median. Do not turn model-test runtime or dependency counts into a claimed Google speedup.
