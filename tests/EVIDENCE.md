# Evidence for 0.2.7

One read-only Codex Google Drive profile call returned current-account ID/email/name fields. Actual tool schema and result were inspected; private values were not placed in the repo. This is NOT a verified Claude interface. Claude account ID and actual Claude Google-profile availability/cross-chat stability remain unverified. See IDENTITY_027.md for the distinction and official documentation sources.

The user-reported awkward greeting exposed a gap: previous instructions lacked a sole-participant default. The update adds that contextual default and optional grounded account-to-People mappings without converting inferred recognition into authentication. Shared ambiguity avoids personal-history disclosure and asks only when identity is needed. Existing learning/Docs storage/configuration remains intact.

Local recognition-policy tests cover the five requested scenarios plus conflicting/shared keys, guests, namespace mismatch, changed email, incomplete inventory, duplicate logical representations, mapping idempotence and sensitive-history handling. These are developer policy models, not Claude outputs or a backend shipped with the plugin. Existing storage/migration/History tests remain regression coverage.

Actual fresh-Claude conversations and readable mapping persistence are pending LIVE_027.md. No Cortex or original personal Yori data was modified. No account identifiers or names from the private profile result are embedded in the release. Package/distribution results are separate in LOCAL_CHECKS.txt and MARKETPLACE_INSTALL.md.
