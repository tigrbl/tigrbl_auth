# Validated Execution Report

- Passed: `False`

## Summary

- validated_artifact_count: `1`
- out_of_scope_validated_artifact_count: `0`
- required_validated_inventory_count: `31`
- validated_inventory_present_count: `1`
- validated_inventory_complete: `False`
- runtime_matrix_present_count: `1`
- runtime_matrix_expected_count: `14`
- runtime_matrix_passed_count: `1`
- runtime_matrix_green: `False`
- test_lane_expected_count: `15`
- test_lane_passed_count: `0`
- in_scope_test_lanes_green: `False`
- migration_portability_passed: `False`
- tier3_evidence_rebuilt_from_validated_runs: `False`

## Failures

- Validated artifact inventory is below the required 14 runtime + 15 test lanes + 2 backend-distinct migration threshold.
- Validated clean-room runtime matrix is incomplete.
- Validated in-scope certification lane execution is incomplete.
- Migration portability validation across SQLite and PostgreSQL is missing.

## Warnings

- Tier 3 evidence has not yet been explicitly rebuilt from validated-run manifests.

## Details

- runtime_matrix_missing: `['base@py3.10', 'base@py3.11', 'sqlite-uvicorn@py3.10', 'sqlite-uvicorn@py3.11', 'sqlite-uvicorn@py3.12', 'postgres-hypercorn@py3.10', 'postgres-hypercorn@py3.11', 'postgres-hypercorn@py3.12', 'tigrcorn@py3.11', 'tigrcorn@py3.12', 'devtest@py3.10', 'devtest@py3.11', 'devtest@py3.12']`
- runtime_matrix_present_count: `1`
- test_lane_missing: `['core@py3.10', 'core@py3.11', 'core@py3.12', 'integration@py3.10', 'integration@py3.11', 'integration@py3.12', 'conformance@py3.10', 'conformance@py3.11', 'conformance@py3.12', 'security-negative@py3.10', 'security-negative@py3.11', 'security-negative@py3.12', 'interop@py3.10', 'interop@py3.11', 'interop@py3.12']`
- test_lane_present_count: `0`
- migration_manifest_present: `False`
- required_validated_inventory_count: `31`
- validated_inventory_present_count: `1`
- validated_inventory_complete: `False`
- runtime_evidence: `{'base@py3.12': {'path': 'dist\\validated-runs\\runtime-base-py312.json', 'manifest_passed': True, 'counts_as_passed': True, 'identity': 'base@py312', 'environment_identity_ready': True, 'install_evidence_ready': True, 'runtime_smoke_passed': True, 'application_probe_passed': True, 'surface_probe_passed': True, 'runner_available': None, 'serve_check_passed': None}}`
- test_lane_evidence: `{}`
- migration_evidence: `[]`
- validated_manifests: `['dist\\validated-runs\\runtime-base-py312.json']`
- out_of_scope_validated_manifests: `[]`
- recognized_manifest_paths: `['dist\\validated-runs\\runtime-base-py312.json']`
- ignored_json_paths: `[]`
