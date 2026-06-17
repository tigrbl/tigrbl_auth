# Certification Evidence Index

- Passed: `False`

## Summary

- claim_count: `410`
- fapi_claim_count: `6`
- security_sensitive_claim_count: `40`
- partition_count: `7`
- target_profile_bundle_count: `199`
- clean_checkout: `{'git_available': True, 'clean': False, 'changed_path_count': 18, 'changed_paths': ['compliance/evidence/certification_test_partitions.json', 'compliance/evidence/certification_test_partitions.yaml', 'docs/compliance/certification_evidence_index.json', 'docs/compliance/certification_evidence_index.md', 'docs/compliance/current_state_report.json', 'docs/compliance/current_state_report.md', 'docs/compliance/feature_completeness_report.json', 'docs/compliance/feature_completeness_report.md', 'docs/compliance/install_substrate_report.json', 'docs/compliance/install_substrate_report.md', 'docs/compliance/runtime_profile_report.json', 'docs/compliance/runtime_profile_report.md', 'docs/compliance/truth_chain.json', 'pkgs/tigrbl-identity-cli/src/tigrbl_identity_cli/cli/install_substrate/_models.py', 'tests/unit/test_clean_room_install_substrate.py', 'tox.ini', 'scripts/tox_pip_install.py', 'tests/unit/test_tox_pip_install.py']}`

## Failures

- Security-sensitive claims missing negative proof: cli-flag:issuer, cli-verb:identity.set-password, fapi2-security.issuer-identification, fapi2-security.jar-required, fapi2-security.par-required, fapi2-security.rar-required, fapi2-security.security-bcp, flag:enable_rfc6750_form, flag:enable_rfc6750_query, profile:baseline, profile:camara-security-interoperability, profile:fapi2-message-signing, profile:fapi2-security, profile:fast-udap-security, profile:fdx-csdf-security-model, profile:hardening, profile:peer-claim, profile:production, route:account-password-change, route:authorize, route:par, route:realms-realm-slug-well-known-openid-configuration, route:tenants-tenant-slug-well-known-openid-configuration, route:token, route:token-exchange
