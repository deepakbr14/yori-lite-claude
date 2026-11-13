# Graph exceptions and recovery

Load only for uncertain/partial writes, missing atomic append, incomplete verification, conflicts, reorganization or schema ambiguity. The normal compact save procedure controls encoding.

### Fallback and uncertain outcomes

If atomic multi-tab append is not exposed/verified, use staged payload appends, grouped verification where supported, then a separate commit append and verification. Batch compatible payloads instead of one call per row/tab when possible. Do not claim the fast path in this mode. No permanent configuration flag should make a different connector inherit unverified capabilities.

On a timeout/lost response, do not generate fresh IDs or blindly replay the operation. Resolve all matching row/operation IDs in bounded complete reads. If the full matching committed operation exists, reuse it with NO write. If matching payloads exist but no commit, validate them and resume only missing members/commit using the staged recovery path. If absent with complete coverage, retry the original operation with its original IDs. If conflicting payloads or incomplete visibility remain, preserve both evidence and the uncertainty; stop dependent writes, not unrelated learning. Identical physical duplicates collapse logically by stable row IDs; differing payloads sharing IDs are an integrity failure. No exactly-once delivery guarantee.

Directory is optional. Do NOT append a hint on ordinary learning. In-turn row receipts are enough. Repair/rebuild hints only on an explicit maintenance task or when measured repeated lookup savings justify the write; no semantic save depends on Directory success. Never change permissions to avoid authorization latency. Log platform approval waits separately; Skills cannot guarantee removal of approval prompts.

Current heads for each entity are committed revisions not named as a predecessor by another valid committed revision of that SAME entity. Reject cycles, dangling predecessors and cross-entity predecessors. No predecessor (new entity) means a root; two competing roots remain a conflict. A newer timestamp or bigger version does not supersede a branch. Retired status is an explicit new version; historical versions remain. Missing dependencies make recall incomplete, not an unset preference.

Two writers reading A may append B→A and C→A. Both survive; B and C are heads. A later D→[B,C] may reconcile them with reasons. A third unseen E→A still remains a head. A commit prepared from an earlier view never claims global exclusivity. Concurrent additions use distinct IDs; uniqueness is not server-enforced. No exactly-once delivery, immutable ACL, snapshot isolation or compare-and-swap is claimed.

## Directory and direct addressing

Directory contains immutable hints: node_id, revision_id, physical row, operation_id and verification time. Never use row position as identity. Read a hinted full Nodes row and verify BOTH node_id and revision_id, payload and commit. On mismatch, discard the hint and locate the ID through actual search or paginated bounded scans; append a corrected hint if useful. Do not return another node or rewrite the stale hint.

Matching IDs alone do not prove the latest state. Before presenting CURRENT memory, discover all matching node versions and their commit state in a complete bounded search/scan, including subsequent versions/branches. A same-turn complete query may be reused until relevant change; fresh chats refresh. Directory alone is never a complete authoritative index. Human sorting/moves require pointer recovery; deletion or edits of immutable evidence are integrity failures, not permission to recreate an assumed memory. The protocol never sorts storage tabs.

## Retrieval and graph traversal

Fetch only needed columns/ranges/pages, not the entire workbook every turn. Resolve config once per fresh chat. At activation discover Self-kind nodes, then read their current heads and relevant context before identity claims. Preserve independent development and the distinction between established preference, deliberate revision and incomplete recall. Person matching uses existing recognition rules and stable People node IDs; count logical participants, not versions or people merely mentioned.

Known ID: try a verified Directory hint or direct range; verify identity and commit; then check head completeness. Unknown ID: bounded kind/title/subject/content search; exact-filter returned rows locally because substring searches also match references. Read full matching rows and their commits, not snippets. A search hit or History event is not the authoritative current node. If the search is truncated, page/partition safely and mark incomplete until coverage is complete. Use observed grid bounds and actual tool limits; the Codex 50,000-cell search cap is not a Claude guarantee.

Edges: discover BOTH from_node_id and to_node_id matches, resolve active committed edge heads, validate endpoints and evidence. For one hop, deduplicate neighbor IDs and bulk-read their full current heads where supported. For two hops, repeat from the one-hop frontier with visited sets; do not assume transitivity or fabricate an edge between the endpoints of a path. Cycles are normal in relationships, not in revision ancestry. Cap retrieval according to the task, but report partial coverage rather than claiming all incoming/outgoing edges when a limit is reached. High-degree nodes require pagination; do not impose a silent edge-count cutoff.

Current Self/People/Knowledge nodes are first authorities; History supplies provenance and prior meaning. Retrieve decision nodes plus explicitly referenced supporting contributions/versions. Preserve unresolved disagreement, dates, commitments and source boundaries. An edge is an attributed assertion, not proof its inferred relation is fact. Unresolved branches of either a node or edge remain visible in the answer when relevant.

## Learning and organization

Selectively learn during ordinary conversation, including meaningful Self choices. After reading relevant existing nodes, consider edges only for actual supported relationships such as supports, contradicts, about, revises, or depends_on; relation words must match the evidence. No automatic all-pairs similarity links, guessed motives or edge-count targets. A correction can preserve the entity ID and append a version and linked History; inferred relationships identify Yori as inference author.

Splitting a topic creates complete new nodes with evidence-backed relationships and an explicit source-node version explaining the change; merging must preserve all source content, uncertainty and identities. Never merge distinct People by name. Preserve references to old nodes and all later competing contributions. Retire through new versions, never row deletion. No routine reorganization after each response.

Quietly finish authorized work and verification. Explain actual unresolved errors concisely, distinguish pending from committed learning, and avoid routine tool-operation narration. No unverified save claims and no reduction of learning to meet latency targets.
