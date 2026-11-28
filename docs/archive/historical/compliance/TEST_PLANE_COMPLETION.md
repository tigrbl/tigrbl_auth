<!-- NON_AUTHORITATIVE_HISTORICAL -->

> [!WARNING]
> Historical checkpoint / planning note — non-authoritative for the current release.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` for current release truth.

> [!WARNING] Historical / non-authoritative document. This file is retained for provenance or implementation context only. Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports for current release truth.

> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# TEST_PLANE_TEST_PLANE_COMPLETION

## Scope completed

This checkpoint completes the test-plane checkpoint workstream for test-plane normalization and certification usability.

## Repository changes

- migrated all legacy `tests/i9n/` test modules into `tests/integration/`
- introduced the canonical manifest `compliance/mappings/test_classification.yaml`
- retained `compliance/mappings/test-classification.yaml` as a compatibility mirror
- expanded `compliance/mappings/target-to-test.yaml` to cover the test-plane checkpoint integration additions and the moved integration suite
- added integration coverage for profile/contract alignment, durable lifecycle persistence, and migration safety
- updated `pyproject.toml` to register the `integration` pytest marker instead of the legacy `i9n` marker
- advanced `compliance/mappings/current-to-target-paths.yaml` so the `tests/i9n -> tests/integration` move is now marked completed
- advanced `compliance/targets/certification_scope.yaml` to `test-plane-evidence`

## test-plane checkpoint verification completed in this checkpoint

The following dependency-light checks were executed successfully from the committed repository state:

- `scripts/verify_test_classification.py`
- `scripts/verify_target_test_mapping.py`
- `scripts/generate_test_coverage_heatmap.py`
- `scripts/verify_target_module_mapping.py`
- `scripts/verify_target_route_mapping.py`
- `scripts/verify_target_contract_mapping.py`
- `scripts/verify_target_evidence_mapping.py`
- `scripts/verify_contract_sync.py`
- `scripts/verify_feature_surface_modularity.py`
- `scripts/verify_project_tree_layout.py`
- `scripts/verify_migration_plan.py`

## Result

test-plane checkpoint closes the classification-completeness gap that previously prevented the test corpus from being used cleanly for certification traceability. The repository now has a canonical test manifest, complete target mappings for the retained boundary, and a committed target coverage heatmap.

## Remaining blockers outside test-plane checkpoint

This checkpoint still does not justify a final truthful claim that the package is certifiably fully featured or certifiably fully RFC/spec compliant across the full retained boundary. The remaining blockers are still dominated by:

- Tier 3 preserved evidence promotion
- Tier 4 independent peer validation
- certification-grade release signing and attestation
- broader execution and evidence promotion for bounded/helper targets such as RFC 7516, RFC 7521, and RFC 7523
