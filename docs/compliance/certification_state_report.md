# Certification State Report

- Passed: `False`

## Summary

- fully_certifiable_now: `False`
- fully_rfc_compliant_now: `False`
- protocol_boundary_tier3_complete: `True`
- retained_boundary_tier3_complete: `True`
- strict_independent_claims_ready: `False`
- authoritative_scope_manifest: `compliance/targets/certification_scope.yaml`
- boundary_freeze_active: `True`
- boundary_freeze_passed: `True`
- boundary_freeze_decision_id: `BND-012`
- boundary_freeze_effective_date: `2026-03-26`
- boundary_freeze_retained_target_count: `48`
- boundary_freeze_rfc_target_count: `30`
- boundary_freeze_non_rfc_target_count: `18`
- boundary_freeze_deferred_target_count: `25`
- boundary_freeze_identity_hash_matches: `True`
- clean_room_matrix_implemented: `True`
- clean_room_matrix_executed_in_this_container: `False`
- tox_manifest_present: `True`
- test_extra_present: `True`
- tigrcorn_pin_committed: `True`
- operator_plane_backend: `sqlite-authoritative`
- operator_plane_repo_mutation_dependency: `False`
- operator_plane_tenancy_enforced: `True`
- tier4_supported_peer_profile_count: `16`
- tier4_required_external_bundle_count: `16`
- tier4_external_bundle_count: `16`
- tier4_valid_external_bundle_count: `0`
- tier4_invalid_external_bundle_count: `16`
- tier4_missing_external_bundle_count: `0`
- tier4_peer_bundle_completeness_passed: `False`
- tier4_external_handoff_template_present: `False`
- tier3_ready_targets: `['ASGI 3 application package', 'Bootstrap and migration lifecycle', 'CLI operator surface', 'Import/export portability', 'Key lifecycle and JWKS publication', 'OIDC Back-Channel Logout', 'OIDC Core 1.0', 'OIDC Discovery 1.0', 'OIDC Front-Channel Logout', 'OIDC RP-Initiated Logout', 'OIDC Session Management', 'OIDC UserInfo', 'OpenAPI 3.1 / 3.2 compatible public contract', 'OpenRPC 1.4.x admin/control-plane contract', 'RFC 6265', 'RFC 6749', 'RFC 6750', 'RFC 7009', 'RFC 7515', 'RFC 7516', 'RFC 7517', 'RFC 7518', 'RFC 7519', 'RFC 7521', 'RFC 7523', 'RFC 7591', 'RFC 7592', 'RFC 7636', 'RFC 7662', 'RFC 8252', 'RFC 8414', 'RFC 8615', 'RFC 8628', 'RFC 8693', 'RFC 8705', 'RFC 8707', 'RFC 9068', 'RFC 9101', 'RFC 9126', 'RFC 9207', 'RFC 9396', 'RFC 9449', 'RFC 9700', 'RFC 9728', 'Release bundle and signature verification', 'Runner profile: Hypercorn', 'Runner profile: Tigrcorn', 'Runner profile: Uvicorn']`
- tier4_ready_targets: `[]`
- validated_execution_artifact_count: `0`
- required_validated_inventory_count: `31`
- validated_inventory_present_count: `0`
- validated_inventory_complete: `False`
- clean_room_matrix_green: `False`
- in_scope_test_lanes_green: `False`
- migration_portability_passed: `False`
- tier3_evidence_rebuilt_from_validated_runs: `False`
- open_gaps: `['Tier 4 independent peer validation is not complete for the retained boundary.', 'The fill-in external handoff template package is not present for the full supported peer-profile set.', 'The peer-bundle completeness gate is not satisfied for the declared peer-profile set.', 'One or more supported peer profiles have incomplete or invalid preserved external evidence bundles.', 'The runtime validation stack now executes real app-factory, serve-check, and HTTP surface probes in the clean-room matrix, but successful execution across the supported interpreter/profile matrix is not preserved in this container.', 'Tigrcorn is now pinned and included in the clean-room matrix for Python 3.11/3.12, but preserved independent validation artifacts remain absent.', 'Validated clean-room install matrix evidence is incomplete or missing.', 'Validated in-scope certification lane execution evidence is incomplete or missing.', 'Migration upgrade → downgrade → reapply portability has not been preserved for both SQLite and PostgreSQL.', 'Tier 3 evidence has not yet been explicitly rebuilt from validated-run manifests.', 'Current generated public artifacts still drift from executable reality.', 'One or more exported package capabilities still lacks end-to-end verification in the current environment.', 'Release evidence can now be built only from a clean checkout, and the current workspace is dirty.']`

## Details

- Tier 4 independent peer validation is not complete for the retained boundary.
- The fill-in external handoff template package is not present for the full supported peer-profile set.
- The peer-bundle completeness gate is not satisfied for the declared peer-profile set.
- One or more supported peer profiles have incomplete or invalid preserved external evidence bundles.
- The runtime validation stack now executes real app-factory, serve-check, and HTTP surface probes in the clean-room matrix, but successful execution across the supported interpreter/profile matrix is not preserved in this container.
- Tigrcorn is now pinned and included in the clean-room matrix for Python 3.11/3.12, but preserved independent validation artifacts remain absent.
- Validated clean-room install matrix evidence is incomplete or missing.
- Validated in-scope certification lane execution evidence is incomplete or missing.
- Migration upgrade → downgrade → reapply portability has not been preserved for both SQLite and PostgreSQL.
- Tier 3 evidence has not yet been explicitly rebuilt from validated-run manifests.
- Current generated public artifacts still drift from executable reality.
- One or more exported package capabilities still lacks end-to-end verification in the current environment.
- Release evidence can now be built only from a clean checkout, and the current workspace is dirty.
