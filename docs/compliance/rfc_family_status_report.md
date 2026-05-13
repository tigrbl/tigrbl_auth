# RFC Family Status Report

- Passed: `False`

## Summary

- rfc_target_count: `30`
- rfc_family_count: `5`
- supported_py311_lane_count_green: `0`
- validated_runtime_matrix_green: `True`
- validated_in_scope_test_lanes_green: `False`
- migration_portability_passed: `True`
- fully_rfc_compliant_now: `False`
- rfc_targets_with_scope_discrepancies: `0`
- rfc_targets_with_conformance_coverage: `30`
- rfc_targets_with_peer_profile_mapping: `30`

## Family summaries

### oauth-core-metadata-discovery

- target_count: `5`
- conformance_coverage: `5` / `5`
- integration_or_security_coverage: `5` / `5`
- interop_coverage: `3` / `5`
- peer_profile_mapping: `5` / `5`
- route_metadata_aligned: `5` / `5`

### jose-jwt

- target_count: `5`
- conformance_coverage: `5` / `5`
- integration_or_security_coverage: `0` / `5`
- interop_coverage: `0` / `5`
- peer_profile_mapping: `5` / `5`
- route_metadata_aligned: `5` / `5`

### revocation-introspection-registration

- target_count: `4`
- conformance_coverage: `4` / `4`
- integration_or_security_coverage: `4` / `4`
- interop_coverage: `0` / `4`
- peer_profile_mapping: `4` / `4`
- route_metadata_aligned: `4` / `4`

### native-device-exchange-resource-jwt-at

- target_count: `5`
- conformance_coverage: `5` / `5`
- integration_or_security_coverage: `4` / `5`
- interop_coverage: `4` / `5`
- peer_profile_mapping: `5` / `5`
- route_metadata_aligned: `5` / `5`

### hardening-advanced-auth-metadata

- target_count: `11`
- conformance_coverage: `11` / `11`
- integration_or_security_coverage: `9` / `11`
- interop_coverage: `6` / `11`
- peer_profile_mapping: `11` / `11`
- route_metadata_aligned: `11` / `11`

## RFC-specific gaps still open


## Global blockers outside the RFC mapping layer

- supported runtime-matrix execution is still incomplete
- supported certification-lane execution is still incomplete across Python 3.10 and 3.12
- migration portability is still incomplete for PostgreSQL and unsupported for certification in this container
- Tier 3 rebuild-from-validated-runs and Tier 4 external peer bundles are still incomplete

## Detail artifact

- JSON: `docs\compliance\rfc_family_status_report.json`
