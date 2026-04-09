# Truth Chain

This manifest is the single generated checkpoint truth for current-state and release-decision artifacts.

- generated_at: `2026-04-09`
- final_release_ready: `False`
- checkpoint_only: `True`
- release_gates_passed: `False`
- final_release_gate_passed: `False`

## Source of truth

- `docs/compliance/current_state_report.json`
- `docs/compliance/certification_state_report.json`
- `docs/compliance/release_gate_report.json`
- `docs/compliance/final_release_gate_report.json`
- `docs/compliance/non_rfc_status_report.json`
- `compliance/targets/document-authority.yaml`

## Summary

- declared_claim_count: `48`
- tier_3_claim_count: `48`
- tier_4_claim_count: `0`
- validated_inventory_complete: `True`
- validated_runtime_matrix_green: `True`
- validated_test_lanes_green: `True`
- migration_portability_passed: `True`
- tier3_evidence_rebuilt_from_validated_runs: `True`
- fully_featured_package_boundary_now: `False`
- strict_independent_claims_ready: `False`
- fully_certifiable_now: `False`
- fully_rfc_compliant_now: `False`
- fully_non_rfc_spec_compliant_now: `False`
- release_gates_passed: `False`
- release_gate_count: `25`
- release_gate_failed_count: `7`
- final_release_gate_passed: `False`
- final_release_ready: `False`
- checkpoint_only: `True`
- target_profile_truth_reconciled_complete: `True`
- profile_scope_mismatch_set_empty: `True`
- clean_room_executor_matrix_declared_complete: `True`
- validated_manifest_identity_contract_installed: `True`
- claim_registry_canonical_complete: `True`
- fapi2_security_profile_declared_complete: `True`
- release_claims_machine_derivable: `True`
- core_targets_missing_from_feature_map: `0`
- extension_targets_missing_from_feature_map: `0`
- settings_backed_flags_missing_from_flag_map: `0`
- tier4_external_bundle_count: `16`
- tier4_valid_external_bundle_count: `0`
- tier4_invalid_external_bundle_count: `16`
- tier4_missing_external_bundle_count: `0`
- open_gaps: `['Tier 4 independent peer validation is not complete for the retained boundary.', 'The peer-bundle completeness gate is not satisfied for the declared peer-profile set.', 'One or more supported peer profiles have incomplete or invalid preserved external evidence bundles.', 'One or more operator-visible package capabilities still lacks end-to-end verification in the current environment.', 'Release evidence can now be built only from a clean checkout, and the current workspace is dirty.']`
- final_release_failures: `['Migration portability validation is not preserved for both SQLite and PostgreSQL.']`
- final_release_warnings: `['Tier 4 bundle promotion is not complete for the retained boundary.']`
- explicitly_deauthorized_current_adjacent_doc_count: `8`

## Explicitly deauthorized current-adjacent docs

- `docs/compliance/BOUNDARY_FREEZE_DECISION_2026-03-26.md`
- `docs/compliance/CLEAN_ROOM_EXECUTOR_AND_EVIDENCE_CHECKPOINT_2026-03-27.md`
- `docs/compliance/STEP12_FINAL_CERTIFICATION_AGGREGATION_CHECKPOINT_2026-03-27.md`
- `docs/compliance/PEER_MATRIX_REPORT.md`
- `docs/compliance/TIER4_PROMOTION_MATRIX.md`
- `docs/compliance/CERTIFIABLE_COMPLETION_PLAN_2026-03-26.md`
- `docs/compliance/CERTIFIABLE_DELIVERY_PLAN_2026-03-27.md`
- `docs/compliance/TARGET_REALITY_MATRIX.md`
