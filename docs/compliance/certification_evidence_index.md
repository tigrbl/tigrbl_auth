# Certification Evidence Index

- Passed: `False`

## Summary

- claim_count: `395`
- fapi_claim_count: `6`
- security_sensitive_claim_count: `37`
- partition_count: `7`
- target_profile_bundle_count: `195`
- clean_checkout: `{'git_available': True, 'clean': False, 'changed_path_count': 34, 'changed_paths': ['Dockerfile.dev-tigrbl', 'compliance/claims/repository-state.yaml', 'compliance/evidence/certification_test_partitions.json', 'compliance/evidence/certification_test_partitions.yaml', 'compliance/targets/document-authority.yaml', 'constraints/base.txt', 'constraints/dependency-lock.json', 'docs/compliance/certification_evidence_index.json', 'docs/compliance/certification_evidence_index.md', 'docs/compliance/current_state_report.json', 'docs/compliance/current_state_report.md', 'docs/compliance/feature_completeness_report.json', 'docs/compliance/feature_completeness_report.md', 'docs/compliance/install_substrate_report.json', 'docs/compliance/install_substrate_report.md', 'docs/compliance/runtime_profile_report.json', 'docs/compliance/runtime_profile_report.md', 'docs/compliance/tigrbl_runtime_foundation_report.json', 'docs/compliance/tigrbl_runtime_foundation_report.md', 'docs/compliance/truth_chain.json', 'docs/compliance/truth_chain.md', 'docs/runbooks/DOCKER_LOCAL_RUNTIME.md', 'docs/runbooks/TIGRBL_UNRESOLVED_SECURITY_CONTRACT_ISSUES.md', 'tests/integration/test_sqlite_attachment_admin_directory.py', 'tests/unit/test_openapi_examples.py', 'tests/unit/test_provenance_naming_guard.py', 'tests/unit/test_published_dependency_model.py', 'tests/unit/test_rfc6749_token_endpoint.py', 'tests/unit/test_rfc8707_resource_indicators.py', 'tigrbl_auth/framework.py', 'tigrbl_auth/migrations/runtime.py', 'tigrbl_auth/ops/token.py', 'tigrbl_auth/rfc/rfc6749_token.py', 'tigrbl_auth/tables/__init__.py']}`

## Failures

- Security-sensitive claims missing negative proof: cli-flag:issuer, cli-verb:identity.set-password, fapi2-security.issuer-identification, fapi2-security.jar-required, fapi2-security.par-required, fapi2-security.rar-required, fapi2-security.security-bcp, flag:enable_rfc6750_form, flag:enable_rfc6750_query, profile:baseline, profile:camara-security-interoperability, profile:fapi2-message-signing, profile:fapi2-security, profile:fast-udap-security, profile:fdx-csdf-security-model, profile:hardening, profile:peer-claim, profile:production, route:authorize, route:par, route:token, route:token-exchange, route:well-known-openid-configuration, slice:par, target:camara-security-and-interoperability-profile
