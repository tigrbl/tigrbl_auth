> **Historical / non-authoritative** — This document is retained for planning, provenance, or operator guidance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# Historical doc authority status — 2026-03-25

This note summarizes the Item 10 historical-drift cleanup and documentation-authority policy.

## Current authority model

- authoritative current docs are defined in `compliance/targets/document-authority.yaml`
- the generated authority index is `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`
- certification bundles copy only the generated current-state docs listed under `current_release_bundle_docs` in the authority manifest
- historical and superseded planning/reference docs live under `docs/archive/historical/` and are non-authoritative

## Current results

- authoritative current doc stale-ref count outside archive: `0`
- historical doc stale-ref count outside archive: `0`
- archived historical root count: `1`
- archived historical reference doc count: `17`

## Archived legacy references that previously drove stale-ref noise

- `docs/archive/historical/reference/RFC_FEATURE_FAMILY_IMPLEMENTATION.md`
- `docs/archive/historical/reference/tigrbl_auth_cli_flag_examples.md`
- `docs/archive/historical/reference/tigrbl_auth_cli_flags.md`
- `docs/archive/historical/reference/tigrbl_auth_full_module_tree.md`
- `docs/archive/historical/reference/tigrbl_auth_project_tree_current_to_target.md`
- `docs/archive/historical/reference/tigrbl_auth_unified_canonical_reference.md`

## Archived historical reference set

- `docs/archive/historical/reference/BROWSER_SESSION_LOGOUT_FLOWS.md`
- `docs/archive/historical/reference/HARDENING_RUNTIME_ENFORCEMENT_MATRIX.md`
- `docs/archive/historical/reference/PERSISTENCE_MODEL.md`
- `docs/archive/historical/reference/README.md`
- `docs/archive/historical/reference/RFC_FEATURE_FAMILY_IMPLEMENTATION.md`
- `docs/archive/historical/reference/tigrbl_auth_authnz_matrices.md`
- `docs/archive/historical/reference/tigrbl_auth_cli_competitor_and_master_surface.md`
- `docs/archive/historical/reference/tigrbl_auth_cli_flag_examples.md`
- `docs/archive/historical/reference/tigrbl_auth_cli_flags.md`
- `docs/archive/historical/reference/tigrbl_auth_full_module_tree.md`
- `docs/archive/historical/reference/tigrbl_auth_implementation_plan.md`
- `docs/archive/historical/reference/tigrbl_auth_project_tree_current_to_target.md`
- `docs/archive/historical/reference/tigrbl_auth_recommended_serve_flags.md`
- `docs/archive/historical/reference/tigrbl_auth_serve_flags_expanded.md`
- `docs/archive/historical/reference/tigrbl_auth_standards_compliance_matrix_v2.md`
- `docs/archive/historical/reference/tigrbl_auth_unified_canonical_reference.md`
- `docs/archive/historical/reference/tigrbl_auth_usage_examples.md`

## Release-bundle documentation scope

- generated current-state docs remain authoritative in the certification bundle
- historical docs and runbook/reference markdown are excluded from bundle documentation scope
