# Validated Execution Report

- Passed: `False`

## Summary

- validated_artifact_count: `2`
- out_of_scope_validated_artifact_count: `0`
- required_validated_inventory_count: `31`
- validated_inventory_present_count: `2`
- validated_inventory_complete: `False`
- runtime_matrix_present_count: `0`
- runtime_matrix_expected_count: `14`
- runtime_matrix_passed_count: `0`
- runtime_matrix_green: `False`
- test_lane_expected_count: `15`
- test_lane_passed_count: `0`
- in_scope_test_lanes_green: `False`
- migration_portability_passed: `True`
- tier3_evidence_rebuilt_from_validated_runs: `False`

## Failures

- Validated artifact inventory is below the required 14 runtime + 15 test lanes + 2 backend-distinct migration threshold.
- Validated clean-room runtime matrix is incomplete.
- Validated in-scope certification lane execution is incomplete.

## Warnings

- Tier 3 evidence has not yet been explicitly rebuilt from validated-run manifests.

## Details

- runtime_matrix_missing: `['base@py3.10', 'base@py3.11', 'base@py3.12', 'sqlite-uvicorn@py3.10', 'sqlite-uvicorn@py3.11', 'sqlite-uvicorn@py3.12', 'postgres-hypercorn@py3.10', 'postgres-hypercorn@py3.11', 'postgres-hypercorn@py3.12', 'tigrcorn@py3.11', 'tigrcorn@py3.12', 'devtest@py3.10', 'devtest@py3.11', 'devtest@py3.12']`
- runtime_matrix_present_count: `0`
- test_lane_missing: `['core@py3.10', 'core@py3.11', 'core@py3.12', 'integration@py3.10', 'integration@py3.11', 'integration@py3.12', 'conformance@py3.10', 'conformance@py3.11', 'conformance@py3.12', 'security-negative@py3.10', 'security-negative@py3.11', 'security-negative@py3.12', 'interop@py3.10', 'interop@py3.11', 'interop@py3.12']`
- test_lane_present_count: `0`
- migration_manifest_present: `True`
- required_validated_inventory_count: `31`
- validated_inventory_present_count: `2`
- validated_inventory_complete: `False`
- runtime_evidence: `{}`
- test_lane_evidence: `{}`
- migration_evidence: `[{'path': 'dist/validated-runs/migration-portability-py312.json', 'manifest_passed': True, 'counts_as_passed': True, 'identity': 'migration-portability@py312', 'environment_identity_ready': True, 'install_evidence_ready': True, 'backends': ['sqlite', 'postgres'], 'passed_backends': ['sqlite', 'postgres'], 'expected_head_revision': '0033_replay_reservations', 'downgrade_target_revision': '0032_claim_definition_and_provenance'}, {'backend': 'postgres', 'counts_as_passed': True, 'manifests': [{'path': 'dist/validated-runs/migration-portability-postgres-py312.json', 'manifest_passed': True, 'counts_as_passed': True, 'identity': 'migration-portability-postgres@py312', 'backend': 'postgres', 'environment_identity_ready': True, 'install_evidence_ready': True, 'expected_head_revision': '0033_replay_reservations', 'downgrade_target_revision': '0032_claim_definition_and_provenance'}]}, {'backend': 'sqlite', 'counts_as_passed': True, 'manifests': [{'path': 'dist/validated-runs/migration-portability-sqlite-py312.json', 'manifest_passed': True, 'counts_as_passed': True, 'identity': 'migration-portability-sqlite@py312', 'backend': 'sqlite', 'environment_identity_ready': True, 'install_evidence_ready': True, 'expected_head_revision': '0033_replay_reservations', 'downgrade_target_revision': '0032_claim_definition_and_provenance'}]}]`
- validated_manifests: `['dist/validated-runs/migration-portability-postgres-py312.json', 'dist/validated-runs/migration-portability-sqlite-py312.json']`
- out_of_scope_validated_manifests: `[]`
- recognized_manifest_paths: `['dist/validated-runs/migration-portability-postgres-py312.json', 'dist/validated-runs/migration-portability-py312.json', 'dist/validated-runs/migration-portability-sqlite-py312.json']`
- ignored_json_paths: `[]`
