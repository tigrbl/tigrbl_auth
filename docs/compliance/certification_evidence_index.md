# Certification Evidence Index

- Passed: `False`

## Summary

- claim_count: `410`
- fapi_claim_count: `6`
- security_sensitive_claim_count: `40`
- partition_count: `7`
- target_profile_bundle_count: `199`
- clean_checkout: `{'git_available': True, 'clean': False, 'changed_path_count': 33, 'changed_paths': ['compliance/claims/claim-registry.yaml', 'compliance/claims/effective-target-claims.baseline.yaml', 'compliance/claims/effective-target-claims.fapi2-security.yaml', 'compliance/claims/effective-target-claims.hardening.yaml', 'compliance/claims/effective-target-claims.peer-claim.yaml', 'compliance/claims/effective-target-claims.production.yaml', 'compliance/claims/feature-registry.yaml', 'compliance/evidence/certification_test_partitions.json', 'compliance/evidence/certification_test_partitions.yaml', 'compliance/evidence/claim_proof_bindings.json', 'compliance/evidence/claim_proof_bindings.yaml', 'compliance/evidence/effective-release-evidence.baseline.yaml', 'compliance/mappings/feature-to-evidence.yaml', 'compliance/mappings/feature-to-target.yaml', 'compliance/mappings/feature-to-test.yaml', 'compliance/mappings/flag-to-feature.yaml', 'compliance/targets/document-authority.yaml', 'docs/compliance/artifact_truthfulness_report.json', 'docs/compliance/artifact_truthfulness_report.md', 'docs/compliance/certification_evidence_index.json', 'docs/compliance/certification_evidence_index.md', 'docs/compliance/contract_sync_report.json', 'docs/compliance/contract_sync_report.md', 'docs/compliance/feature_completeness_report.json', 'docs/compliance/feature_completeness_report.md', 'docs/compliance/install_substrate_report.json', 'docs/compliance/install_substrate_report.md', 'docs/compliance/runtime_profile_report.json', 'docs/compliance/runtime_profile_report.md', 'specs/openapi/profiles/baseline/tigrbl_auth.public.openapi.json', 'specs/openapi/profiles/baseline/tigrbl_auth.public.openapi.yaml', 'specs/openapi/tigrbl_auth.public.openapi.json', 'specs/openapi/tigrbl_auth.public.openapi.yaml']}`

## Failures

- Security-sensitive claims missing negative proof: cli-flag:issuer, cli-verb:identity.set-password, fapi2-security.issuer-identification, fapi2-security.jar-required, fapi2-security.par-required, fapi2-security.rar-required, fapi2-security.security-bcp, flag:enable_rfc6750_form, flag:enable_rfc6750_query, profile:baseline, profile:camara-security-interoperability, profile:fapi2-message-signing, profile:fapi2-security, profile:fast-udap-security, profile:fdx-csdf-security-model, profile:hardening, profile:peer-claim, profile:production, route:account-password-change, route:authorize, route:par, route:realms-realm-slug-well-known-openid-configuration, route:tenants-tenant-slug-well-known-openid-configuration, route:token, route:token-exchange
