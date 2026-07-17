<!-- NON_AUTHORITATIVE_HISTORICAL -->
> [!WARNING]
> Historical / non-authoritative checkpoint document.
> Do **not** use this file to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

> [!WARNING] Historical / non-authoritative document. This file is retained for provenance or implementation context only. Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports for current release truth.

> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# Boundary Decision Matrix

| Decision | ADR | Checks | Gates |
|---|---|---|---|
| BND-001 | `ADR-0009-package-boundary-strict-core.md` | claims_linter, declared-target-only-certification | gate-05-governance, gate-15-boundary-enforcement |
| BND-002 | `ADR-0017-plane-modularity.md` | module-boundary-resolution, wrapper_hygiene_scan | gate-00-structure, gate-15-boundary-enforcement, gate-25-wrapper-hygiene |
| BND-003 | `ADR-0005-standards-vs-extensions.md` | claims_linter, extension-quarantine-check, boundary-import-scan | gate-05-governance, gate-15-boundary-enforcement |
| BND-004 | `ADR-0004-no-fastapi-no-starlette.md` | framework_leakage_scan | gate-10-static, gate-15-boundary-enforcement |
| BND-005 | `ADR-0014-tigrbl-public-app-only-composition.md` | framework_leakage_scan, boundary-import-scan | gate-10-static, gate-15-boundary-enforcement |
| BND-006 | `ADR-0019-boundary-enforcement-as-code.md` | wrapper_hygiene_scan, certified_core_wrapper_count_zero | gate-15-boundary-enforcement, gate-25-wrapper-hygiene |
| BND-007 | `ADR-0011-evidence-model-and-tier-promotion.md` | evidence_gate, tier3_claims_have_evidence_refs | gate-40-evidence, gate-45-evidence-peer |
| BND-008 | `ADR-0012-independent-peer-claims.md` | peer_gate, tier4_claims_have_peer_refs | gate-45-evidence-peer, gate-90-release |
| BND-009 | `ADR-0021-project-tree-and-migration-plan.md` | project_tree_layout_check, migration_move_map_check | gate-12-project-tree-layout, gate-18-migration-plan |
