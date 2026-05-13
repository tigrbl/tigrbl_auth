# Test Execution Gate Report

- Passed: `False`

## Summary

- classification_manifest_passed: `False`
- in_scope_test_lanes_green: `False`
- migration_portability_passed: `True`
- validated_test_lane_count: `10`
- validated_test_lane_expected_count: `15`

## Failures

- Test classification manifest is invalid.
- Validated in-scope certification lane execution is incomplete.

## Details

- classification_failures: `['Unclassified test files present: tests/examples/test_python_cli_device_login.py, tests/features/test_profile_reference_union.py, tests/features/test_tenant_jwks_discovery.py, tests/integration/test_admin_auth_session.py, tests/integration/test_admin_table_issue_regressions.py, tests/integration/test_admin_table_surfaces.py, tests/integration/test_default_openapi_endpoints.py, tests/integration/test_profile_all_documented_endpoints.py, tests/integration/test_runtime_issuer_alignment.py, tests/integration/test_sqlite_attachment_admin_directory.py, tests/unit/test_advanced_identity_plane_phase4.py, tests/unit/test_authorization_provenance.py, tests/unit/test_bootstrap_secret_scrub.py, tests/unit/test_governance_extension_plane_phase5.py, tests/unit/test_key_rotation_policy_governance.py, tests/unit/test_path_safety.py, tests/unit/test_policy_control_plane_phase3.py, tests/unit/test_protected_resource_verifier_contract.py, tests/unit/test_release_posture_plane.py, tests/unit/test_request_scoped_runtime_authority.py, tests/unit/test_truth_chain_hashing.py']`
- missing_test_lane_manifests: `['core@py3.11', 'integration@py3.11', 'conformance@py3.11', 'security-negative@py3.11', 'interop@py3.11']`
