# Non-RFC Standards / Specs Status Report

- Passed: `False`

## Summary

- non_rfc_target_count: `18`
- non_rfc_family_count: `4`
- non_rfc_targets_with_scope_discrepancies: `0`
- non_rfc_targets_internally_backed_now: `18`
- focus_py313_report_count: `0`
- focus_py313_passed_tests: `0`
- focus_py313_collected_tests: `0`
- focus_py313_all_passed: `False`
- supported_py311_lane_count_green: `0`
- validated_runtime_matrix_green: `False`
- validated_in_scope_test_lanes_green: `False`
- migration_portability_passed: `False`
- fully_certifiable_now: `False`
- strict_independent_claims_ready: `False`
- certifiably_fully_non_rfc_spec_compliant_now: `False`

## Focus verification artifacts


## Family summaries

### oidc

- target_count: `7`
- internally_backed_now: `7` / `7`
- conformance_coverage: `7` / `7`
- unit_or_integration_coverage: `7` / `7`
- security_coverage: `4` / `7`
- interop_coverage: `1` / `7`
- peer_profile_mapping: `7` / `7`

### contracts

- target_count: `2`
- internally_backed_now: `2` / `2`
- conformance_coverage: `0` / `2`
- unit_or_integration_coverage: `2` / `2`
- security_coverage: `0` / `2`
- interop_coverage: `0` / `2`
- peer_profile_mapping: `2` / `2`

### runtime

- target_count: `4`
- internally_backed_now: `4` / `4`
- conformance_coverage: `4` / `4`
- unit_or_integration_coverage: `4` / `4`
- security_coverage: `0` / `4`
- interop_coverage: `0` / `4`
- peer_profile_mapping: `4` / `4`

### operator-lifecycle

- target_count: `5`
- internally_backed_now: `5` / `5`
- conformance_coverage: `4` / `5`
- unit_or_integration_coverage: `5` / `5`
- security_coverage: `1` / `5`
- interop_coverage: `0` / `5`
- peer_profile_mapping: `5` / `5`

## Remaining non-RFC / package-level blockers

- supported runner-profile certification evidence is still missing for the retained Python 3.10 / 3.11 / 3.12 matrix
- supported certification-lane evidence is still incomplete across all required interpreters
- PostgreSQL migration portability proof is still missing
- Tier 3 rebuild-from-validated-runs and Tier 4 external peer bundles are still incomplete

## Detail artifact

- JSON: `docs\compliance\non_rfc_status_report.json`
