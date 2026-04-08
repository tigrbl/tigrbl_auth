# Release Gate Report

- Passed: `False`

## Summary

- gate_count: `25`
- failed_gate_count: `7`
- validated_execution_artifact_count: `33`
- required_validated_inventory_count: `31`
- validated_inventory_present_count: `31`
- validated_inventory_complete: `True`
- clean_room_install_matrix_green: `True`
- in_scope_test_lanes_green: `True`
- migration_portability_passed: `False`
- tier3_evidence_rebuilt_from_validated_runs: `True`

## Failures

- Gate failed: gate-15-boundary-enforcement
- Gate failed: gate-20-tests
- Gate failed: gate-45-evidence-peer
- Gate failed: gate-60-release-signing (release evidence requires a clean checkout; dirty paths detected: CERTIFICATION_STATUS.md, CURRENT_STATE.md, compliance/claims/issue-registry.yaml, compliance/claims/repository-state.yaml, compliance/evidence/manifest.yaml, compliance/evidence/tier4/bundles/README.md, compliance/evidence/tier4/candidates/assertion-client/execution.log, compliance/evidence/tier4/candidates/assertion-client/manifest.yaml, compliance/evidence/tier4/candidates/assertion-client/mapping.yaml, compliance/evidence/tier4/candidates/assertion-client/peer-artifacts/README.md)
- Gate failed: gate-65-state-reports ([WinError 145] The directory is not empty: 'E:\\swarmauri_github\\tigrbl_auth\\dist\\feature-completeness-sandbox\\release-bundle')
- Gate failed: gate-75-test-classification
- Gate failed: gate-90-release

## Details

- {'gate': 'gate-00-structure', 'passed': True, 'rc': 0}
- {'gate': 'gate-05-governance', 'passed': True, 'rc': 0}
- {'gate': 'gate-08-claim-registry-sync', 'passed': True, 'rc': 0}
- {'gate': 'gate-10-static', 'passed': True, 'rc': 0}
- {'gate': 'gate-12-project-tree-layout', 'passed': True, 'rc': 0}
- {'gate': 'gate-15-boundary-enforcement', 'passed': False, 'rc': 1}
- {'gate': 'gate-18-migration-plan', 'passed': True, 'rc': 0}
- {'gate': 'gate-20-tests', 'passed': False, 'rc': 1}
- {'gate': 'gate-25-wrapper-hygiene', 'passed': True, 'rc': 0}
- {'gate': 'gate-30-contracts', 'passed': True, 'rc': 0}
- {'gate': 'gate-35-contract-sync', 'passed': True, 'rc': 0}
- {'gate': 'gate-40-evidence', 'passed': True, 'rc': 0}
- {'gate': 'gate-45-evidence-peer', 'passed': False, 'rc': 1}
- {'gate': 'gate-50-release-bundle', 'passed': True, 'rc': 0}
- {'gate': 'gate-55-contract-validation', 'passed': True, 'rc': 0}
- {'gate': 'gate-60-release-signing', 'passed': False, 'rc': 1, 'error': 'release evidence requires a clean checkout; dirty paths detected: CERTIFICATION_STATUS.md, CURRENT_STATE.md, compliance/claims/issue-registry.yaml, compliance/claims/repository-state.yaml, compliance/evidence/manifest.yaml, compliance/evidence/tier4/bundles/README.md, compliance/evidence/tier4/candidates/assertion-client/execution.log, compliance/evidence/tier4/candidates/assertion-client/manifest.yaml, compliance/evidence/tier4/candidates/assertion-client/mapping.yaml, compliance/evidence/tier4/candidates/assertion-client/peer-artifacts/README.md'}
- {'gate': 'gate-65-state-reports', 'passed': False, 'rc': 1, 'error': "[WinError 145] The directory is not empty: 'E:\\\\swarmauri_github\\\\tigrbl_auth\\\\dist\\\\feature-completeness-sandbox\\\\release-bundle'"}
- {'gate': 'gate-75-test-classification', 'passed': False, 'rc': 1}
- {'gate': 'gate-85-peer-profiles', 'passed': True, 'rc': 0}
- {'gate': 'gate-87-peer-bundle-completeness', 'passed': True, 'rc': 0}
- {'gate': 'gate-90-release', 'passed': False, 'rc': 1}
- {'gate': 'gate-95-recertification', 'passed': True, 'rc': 0}
- {'gate': 'gate-truth-current-state', 'passed': True, 'rc': 0}
- {'gate': 'gate-truth-release-decision', 'passed': True, 'rc': 0}
- {'gate': 'gate-truth-repository-state', 'passed': True, 'rc': 0}
