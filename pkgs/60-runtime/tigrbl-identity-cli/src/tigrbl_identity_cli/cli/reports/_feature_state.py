from __future__ import annotations

def generate_state_reports(repo_root: Path) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    _ensure_repo_local_operator_state(repo_root)
    claims = _load_yaml(repo_root / "compliance" / "claims" / "declared-target-claims.yaml")
    target_to_module = _load_yaml(repo_root / "compliance" / "mappings" / "target-to-module.yaml")
    target_to_test = _load_yaml(repo_root / "compliance" / "mappings" / "target-to-test.yaml")
    target_to_evidence = _load_yaml(repo_root / "compliance" / "mappings" / "target-to-evidence.yaml")
    scope_path = repo_root / "compliance" / "targets" / "certification_scope.yaml"
    scope = _load_yaml(scope_path) if scope_path.exists() else {}
    scope_freeze_failures, scope_freeze_summary = validate_scope_freeze_metadata(scope) if scope else (["missing certification_scope"], {})
    claim_entries = list(claims.get("claim_set", {}).get("claims", []))
    targets = [str(entry.get("target")) for entry in claim_entries]
    effective_baseline = _load_yaml(repo_root / "compliance" / "claims" / "effective-target-claims.baseline.yaml")
    effective_production = _load_yaml(repo_root / "compliance" / "claims" / "effective-target-claims.production.yaml")
    effective_hardening = _load_yaml(repo_root / "compliance" / "claims" / "effective-target-claims.hardening.yaml")
    tier_counts = {tier: 0 for tier in range(5)}
    tier_by_target: dict[str, int] = {}
    for entry in claim_entries:
        tier = int(entry.get("tier", 0))
        target = str(entry.get("target"))
        tier_counts[tier] = tier_counts.get(tier, 0) + 1
        tier_by_target[target] = tier

    scope_entries = [entry for entry in scope.get("targets", []) if str(entry.get("scope_bucket")) != "out-of-scope/deferred"]
    protocol_targets = [str(entry.get("label")) for entry in scope_entries if str(entry.get("family")) not in {"runtime", "operator"}]
    runtime_targets = [str(entry.get("label")) for entry in scope_entries if str(entry.get("family")) == "runtime"]
    operator_targets = [str(entry.get("label")) for entry in scope_entries if str(entry.get("family")) == "operator"]
    retained_targets = [str(entry.get("label")) for entry in scope_entries]
    baseline_targets = [str(entry.get("label")) for entry in scope_entries if str(entry.get("scope_bucket")) == "baseline-certifiable-now"]
    production_targets = [str(entry.get("label")) for entry in scope_entries if str(entry.get("scope_bucket")) == "production-completion-required"]
    hardening_targets = [str(entry.get("label")) for entry in scope_entries if str(entry.get("scope_bucket")) == "hardening-completion-required"]

    def _count_below_tier(target_names: list[str], *, minimum: int = 3) -> int:
        return sum(1 for name in target_names if tier_by_target.get(name, 0) < minimum)

    all_retained_tier3 = _count_below_tier(retained_targets) == 0
    all_protocol_tier3 = _count_below_tier(protocol_targets) == 0
    strict_independent_claims_ready = _count_below_tier(retained_targets, minimum=4) == 0

    bucket_counts = {
        "baseline_certifiable_now_count": len(baseline_targets),
        "production_completion_required_count": _count_below_tier(production_targets),
        "hardening_completion_required_count": _count_below_tier(hardening_targets),
        "runtime_completion_required_count": _count_below_tier(runtime_targets),
        "operator_completion_required_count": _count_below_tier(operator_targets),
        "retained_targets_below_tier3_count": _count_below_tier(retained_targets),
    }
    signed_bundles = sorted((repo_root / "dist" / "release-bundles").glob("*/*/signature.json")) if (repo_root / "dist" / "release-bundles").exists() else []

    pyproject = _load_pyproject_manifest(repo_root)
    project = pyproject.get("project", {}) if isinstance(pyproject, dict) else {}
    base_dependencies = [str(item) for item in project.get("dependencies", []) or []]
    optional_dependencies = project.get("optional-dependencies", {}) or {}
    workspace_sources = (((pyproject.get("tool", {}) or {}).get("uv", {}) or {}).get("sources", {}) or {}) if isinstance(pyproject, dict) else {}
    runner_extras = {name: list(values) for name, values in optional_dependencies.items() if name in {"uvicorn", "hypercorn", "tigrcorn", "servers"}}
    storage_extras = {name: list(values) for name, values in optional_dependencies.items() if name in {"postgres", "sqlite"}}
    allowed_workspace_sources, forbidden_workspace_sources = _classify_uv_sources(
        repo_root, workspace_sources
    )
    dependency_artifacts = _dependency_artifact_paths(repo_root)
    test_constraints_manifest = repo_root / "constraints" / "test.txt"
    tox_manifest = repo_root / "tox.ini"
    tigrcorn_extra = runner_extras.get("tigrcorn", [])
    runtime_pkg = repo_root / "tigrbl_auth" / "runtime"
    runtime_module_count = len(list(runtime_pkg.glob("*.py"))) if runtime_pkg.exists() else 0
    runner_names = list(registered_runner_names())
    hash_matrix = build_runtime_hash_matrix()
    runner_registry = runner_registry_manifest()
    runtime_profile_report = write_runtime_profile_report(
        repo_root,
        deployment=deployment_from_options(profile="baseline"),
        report_dir=repo_root / "docs" / "compliance",
    )
    install_substrate_report = write_install_substrate_report(
        repo_root,
        report_dir=repo_root / "docs" / "compliance",
    )
    authoritative_docs_manifest = write_authoritative_current_docs_manifest(repo_root)
    run_contract_sync_check(repo_root, strict=False, report_dir=repo_root / "docs" / "compliance")
    run_runtime_foundation_check(repo_root, strict=False, report_dir=repo_root / "docs" / "compliance")
    contract_sync_report = _load_json_if_exists(repo_root / "docs" / "compliance" / "contract_sync_report.json") or {}
    no_fastapi_report = _load_json_if_exists(repo_root / "docs" / "compliance" / "no_fastapi_starlette_report.json") or {}
    artifact_truthfulness = generate_artifact_truthfulness_report(repo_root)
    feature_completeness = build_feature_completeness_report(repo_root, report_dir=repo_root / "docs" / "compliance")
    certification_evidence_index = generate_certification_evidence_index(repo_root)
    peer_bundle_completeness = verify_peer_bundle_completeness(repo_root, strict=False)
    operator_plane = operator_plane_status(repo_root)
    validated_execution = load_validated_execution_status(repo_root)
    peer_matrix_report_path = repo_root / "docs" / "compliance" / "peer_matrix_report.json"
    peer_matrix_report = json.loads(peer_matrix_report_path.read_text(encoding="utf-8")) if peer_matrix_report_path.exists() else {}
    peer_matrix_summary = peer_matrix_report.get("summary", {}) if isinstance(peer_matrix_report, dict) else {}

    current_state = {
        "repository_tier": claims.get("claim_set", {}).get("current_repository_tier", 0),
        "delivery_track": claims.get("claim_set", {}).get("delivery_track", "unknown"),
        "authoritative_scope_manifest": str(scope_path.relative_to(repo_root)) if scope_path.exists() else None,
        "boundary_freeze_active": bool(scope.get("boundary_freeze")),
        "boundary_freeze_passed": not scope_freeze_failures,
        "boundary_freeze_decision_id": str(scope.get("boundary_freeze", {}).get("decision_id", "")),
        "boundary_freeze_effective_date": str(scope.get("boundary_freeze", {}).get("effective_date", "")),
        "boundary_freeze_retained_target_count": int(scope.get("boundary_freeze", {}).get("retained_target_count", 0) or 0),
        "boundary_freeze_rfc_target_count": int(scope.get("boundary_freeze", {}).get("retained_rfc_target_count", 0) or 0),
        "boundary_freeze_non_rfc_target_count": int(scope.get("boundary_freeze", {}).get("retained_non_rfc_target_count", 0) or 0),
        "boundary_freeze_deferred_target_count": int(scope.get("boundary_freeze", {}).get("deferred_target_count", 0) or 0),
        "boundary_freeze_identity_hash_matches": bool(scope_freeze_summary.get("scope_freeze_retained_target_identity_hash_matches", False)),
        "document_authority_manifest": authoritative_docs_manifest.get("projection_manifest"),
        "document_authority_spec": authoritative_docs_manifest.get("authority_spec"),
        "document_authority_projection_manifest": authoritative_docs_manifest.get("projection_manifest"),
        "canonical_ssot_root_count": len(authoritative_docs_manifest.get("canonical_ssot_roots", [])),
        "certification_bundle_current_state_doc_only": True,
        "certification_bundle_generated_current_docs_only": True,
        "authoritative_current_doc_count": len(authoritative_docs_manifest.get("authoritative_current_docs", [])),
        "archived_historical_root_count": len(authoritative_docs_manifest.get("archive_roots", [])),
        "archived_reference_doc_count": len(list((repo_root / "docs" / "archive" / "historical" / "reference").glob("*.md"))) if (repo_root / "docs" / "archive" / "historical" / "reference").exists() else 0,
        "certification_bundle_current_state_doc_count": len(authoritative_docs_manifest.get("certification_bundle_generated_current_docs", [])),
        "declared_claim_count": len(claim_entries),
        "mapped_module_count": sum(1 for target in targets if target in target_to_module),
        "mapped_test_count": sum(1 for target in targets if target in target_to_test),
        "mapped_evidence_count": sum(1 for target in targets if target in target_to_evidence),
        "effective_baseline_count": len(effective_baseline.get("claim_set", {}).get("claims", [])),
        "effective_production_count": len(effective_production.get("claim_set", {}).get("claims", [])),
        "effective_hardening_count": len(effective_hardening.get("claim_set", {}).get("claims", [])),
        "tier_0_claim_count": tier_counts.get(0, 0),
        "tier_1_claim_count": tier_counts.get(1, 0),
        "tier_2_claim_count": tier_counts.get(2, 0),
        "tier_3_claim_count": tier_counts.get(3, 0),
        "tier_4_claim_count": tier_counts.get(4, 0),
        "protocol_boundary_tier3_complete": all_protocol_tier3,
        "retained_boundary_tier3_complete": all_retained_tier3,
        "strict_independent_claims_ready": strict_independent_claims_ready,
        "tier4_peer_bundle_completeness_passed": bool(peer_bundle_completeness.get("passed", False)),
        "tier4_supported_peer_profile_count": int(peer_matrix_summary.get("candidate_profile_count", peer_matrix_summary.get("profile_count", 0))),
        "tier4_required_external_bundle_count": int(peer_matrix_summary.get("candidate_profile_count", peer_matrix_summary.get("profile_count", 0))),
        "tier4_external_bundle_count": int(peer_matrix_summary.get("external_bundle_count", 0)),
        "tier4_valid_external_bundle_count": int(peer_matrix_summary.get("valid_external_bundle_count", peer_matrix_summary.get("external_bundle_count", 0))),
        "tier4_invalid_external_bundle_count": int(peer_matrix_summary.get("invalid_external_bundle_count", 0)),
        "tier4_missing_external_bundle_count": int(peer_matrix_summary.get("missing_external_bundle_count", max(int(peer_matrix_summary.get("candidate_profile_count", peer_matrix_summary.get("profile_count", 0))) - int(peer_matrix_summary.get("external_bundle_count", 0)) - int(peer_matrix_summary.get("invalid_external_bundle_count", 0)), 0))),
        "tier4_external_handoff_template_present": (repo_root / "dist" / "tier4-external-handoff" / "external-root-template.json").exists(),
        "signed_release_bundle_count": len(signed_bundles),
        "release_attestation_verifiable": len(signed_bundles) > 0,
        "base_dependency_count": len(base_dependencies),
        "base_exact_pinned_dependency_count": sum(1 for item in base_dependencies if _is_exact_pin(item)),
        "optional_extra_count": len(optional_dependencies),
        "runner_extra_count": len(runner_extras),
        "storage_extra_count": len(storage_extras),
        "workspace_source_count": len(workspace_sources),
        "workspace_sources_declared": bool(workspace_sources),
        "first_party_workspace_source_count": len(allowed_workspace_sources),
        "forbidden_workspace_source_count": len(forbidden_workspace_sources),
        "workspace_sources_present": bool(forbidden_workspace_sources),
        "dependency_provenance_artifact_count": len(dependency_artifacts),
        "dependency_source": "pyproject.toml",
        "install_substrate_report_present": (repo_root / "docs" / "compliance" / "install_substrate_report.json").exists(),
        "install_substrate_manifest_passed": bool(install_substrate_report.get("summary", {}).get("static_manifest_passed", False)),
        "install_substrate_current_profile": str(install_substrate_report.get("summary", {}).get("profile", "")),
        "install_substrate_current_python_supported": bool(install_substrate_report.get("summary", {}).get("current_python_supported", False)),
        "install_substrate_detected_supported_python_count": int(install_substrate_report.get("summary", {}).get("detected_supported_python_count", 0)),
        "install_substrate_expected_supported_python_count": int(install_substrate_report.get("summary", {}).get("expected_supported_python_count", 0)),
        "install_substrate_tox_env_count": int(install_substrate_report.get("summary", {}).get("declared_certification_tox_env_count", 0)),
        "install_substrate_tox_pip_check_complete": bool(install_substrate_report.get("summary", {}).get("tox_envs_declare_pip_check", False)),
        "install_substrate_tox_import_probe_complete": bool(install_substrate_report.get("summary", {}).get("tox_envs_declare_install_probe", False)),
        "install_substrate_current_profile_import_probe_passed": bool(install_substrate_report.get("summary", {}).get("current_profile_import_probe_passed", False)),
        "test_constraints_manifest_present": test_constraints_manifest.exists(),
        "tox_manifest_present": tox_manifest.exists(),
        "native_uv_lock_present": (repo_root / "uv.lock").exists(),
        "install_profile_workflow_present": has_install_matrix_workflow(repo_root),
        "release_gate_workflow_present": has_release_gate_workflow(repo_root),
        "clean_room_matrix_implemented": tox_manifest.exists() and has_install_matrix_workflow(repo_root) and has_release_gate_workflow(repo_root),
        "clean_room_matrix_executed_in_this_container": False,
        "tigrcorn_extra_placeholder": len(tigrcorn_extra) == 0 and "tigrcorn" in runner_extras,
        "tigrcorn_pin_committed": len(tigrcorn_extra) > 0,
        "runtime_adapter_layer_present": runtime_pkg.exists(),
        "runtime_adapter_module_count": runtime_module_count,
        "registered_runner_count": len(runner_names),
        "registered_runner_names": ", ".join(runner_names),
        "runtime_application_hash_invariant": len({item["application_hash"] for item in hash_matrix.values()}) == 1,
        "runtime_runner_availability_count": len([item for item in runner_registry if item.get("installed")]),
        "runtime_profile_report_present": (repo_root / "docs" / "compliance" / "runtime_profile_report.json").exists(),
        "runtime_profile_ready_count": int(runtime_profile_report.get("summary", {}).get("ready_count", 0)),
        "runtime_profile_missing_count": int(runtime_profile_report.get("summary", {}).get("missing_count", 0)),
        "runtime_profile_invalid_count": int(runtime_profile_report.get("summary", {}).get("invalid_count", 0)),
        "runtime_profile_application_probe_passed": bool(runtime_profile_report.get("application_probe", {}).get("passed", False)),
        "runtime_profile_surface_probe_passed": bool(runtime_profile_report.get("summary", {}).get("surface_probe_passed", False)),
        "runtime_profile_surface_probe_endpoint_count": int(runtime_profile_report.get("summary", {}).get("surface_probe_endpoint_count", 0)),
        "runtime_profile_surface_probe_passed_count": int(runtime_profile_report.get("summary", {}).get("surface_probe_passed_count", 0)),
        "runtime_profile_surface_probe_failed_count": int(runtime_profile_report.get("summary", {}).get("surface_probe_failed_count", 0)),
        "runtime_profile_serve_check_passed_count": int(runtime_profile_report.get("summary", {}).get("serve_check_passed_count", 0)),
        "runtime_profile_execution_probe_complete": bool(runtime_profile_report.get("summary", {}).get("execution_probe_complete", False)),
        "runtime_profile_placeholder_supported_runner_count": int(runtime_profile_report.get("summary", {}).get("placeholder_supported_runner_count", 0)),
        "runtime_profile_declared_ci_installable_runner_count": int(runtime_profile_report.get("summary", {}).get("declared_ci_installable_runner_count", 0)),
        "runtime_profile_declared_ci_install_probe_complete": bool(runtime_profile_report.get("summary", {}).get("declared_ci_install_probe_complete", False)),
        "operator_plane_backend": str(operator_plane.get("backend", "unknown")),
        "operator_plane_repo_mutation_dependency": bool(operator_plane.get("repo_mutation_dependency", True)),
        "operator_plane_tenancy_enforced": bool(operator_plane.get("tenancy_enforced", False)),
        "operator_plane_database_present": bool(operator_plane.get("database_present", False)),
        "operator_plane_state_root": str(operator_plane.get("state_root", "")),
        "operator_plane_portability_schema_version": int(operator_plane.get("portability_schema_version", 0) or 0),
        "pyproject_requires_python": str(project.get("requires-python", "unspecified")),
        "serve_runtime_launcher_present": True,
        "cli_contract_artifact_present": (repo_root / "specs" / "cli" / "cli_contract.json").exists(),
        "cli_contract_snapshot_present": (repo_root / "docs" / "compliance" / "cli_conformance_snapshot.json").exists(),
        "cli_help_snapshot_present": (repo_root / "docs" / "compliance" / "cli_conformance_snapshot.md").exists(),
        "cli_command_count": int(build_cli_contract_manifest().get("summary", {}).get("command_count", 0)),
        "cli_verb_count": int(build_cli_contract_manifest().get("summary", {}).get("verb_count", 0)),
        "cli_catalog_only_resource_command_count": len(build_cli_conformance_snapshot().get("summary", {}).get("catalog_only_resource_commands", [])),
        "cli_required_verbs_missing": bool(build_cli_conformance_snapshot().get("summary", {}).get("missing_required_verbs", {})),
        "artifact_truthfulness_passed": bool(artifact_truthfulness.get("passed", False)),
        "contract_sync_report_passed": bool(contract_sync_report.get("passed", False)),
        "contract_to_route_sync_passed": bool(artifact_truthfulness.get("summary", {}).get("contract_to_route_sync_passed", False)),
        "route_to_contract_sync_passed": bool(artifact_truthfulness.get("summary", {}).get("route_to_contract_sync_passed", False)),
        "target_to_contract_sync_passed": bool(artifact_truthfulness.get("summary", {}).get("target_to_contract_sync_passed", False)),
        "cli_metadata_to_docs_sync_passed": bool(artifact_truthfulness.get("summary", {}).get("cli_metadata_to_docs_sync_passed", False)),
        "runtime_plan_to_discovery_sync_passed": bool(artifact_truthfulness.get("summary", {}).get("runtime_plan_to_discovery_sync_passed", False)),
        "runner_contract_hash_invariance_passed": bool(artifact_truthfulness.get("summary", {}).get("runner_contract_hash_invariance_passed", False)),
        "no_fastapi_starlette_passed": bool(feature_completeness.get("summary", {}).get("no_fastapi_starlette_passed", False)),
        "feature_completeness_capability_count": int(feature_completeness.get("summary", {}).get("capability_count", 0)),
        "feature_completeness_passed_capability_count": int(feature_completeness.get("summary", {}).get("passed_capability_count", 0)),
        "feature_completeness_failed_capability_count": int(feature_completeness.get("summary", {}).get("failed_capability_count", 0)),
        "fully_featured_package_boundary_now": bool(feature_completeness.get("summary", {}).get("fully_featured_package_boundary_now", False)),
        "feature_release_verify_verb_present": bool(feature_completeness.get("summary", {}).get("required_release_verify_verb_present", False)),
        "certification_evidence_index_passed": bool(certification_evidence_index.get("passed", False)),
        "certification_evidence_claim_count": int(certification_evidence_index.get("summary", {}).get("claim_count", 0)),
        "certification_evidence_partition_count": int(certification_evidence_index.get("summary", {}).get("partition_count", 0)),
        "certification_evidence_target_profile_bundle_count": int(certification_evidence_index.get("summary", {}).get("target_profile_bundle_count", 0)),
        "release_evidence_clean_checkout_required": True,
        "release_evidence_clean_checkout_now": bool(certification_evidence_index.get("summary", {}).get("clean_checkout", {}).get("clean", False)),
        "release_evidence_dirty_checkout_path_count": int(certification_evidence_index.get("summary", {}).get("clean_checkout", {}).get("changed_path_count", 0)),
        "authoritative_current_doc_stale_ref_count": int(artifact_truthfulness.get("summary", {}).get("authoritative_current_doc_stale_ref_count", 0)),
        "historical_doc_stale_ref_count": int(artifact_truthfulness.get("summary", {}).get("historical_doc_stale_ref_count", 0)),
        "authoritative_current_doc_count": len(authoritative_docs_manifest.get("authoritative_current_docs", [])),
        "derived_current_doc_count": len(authoritative_docs_manifest.get("derived_current_docs", [])),
        "historical_archive_present": (repo_root / "docs" / "archive").exists(),
        "certification_bundle_generated_current_docs_only": True,
        "validated_execution_artifact_count": int(validated_execution.get("validated_artifact_count", 0)),
        "required_validated_inventory_count": int(validated_execution.get("required_validated_inventory_count", 0)),
        "validated_inventory_present_count": int(validated_execution.get("validated_inventory_present_count", 0)),
        "validated_inventory_complete": bool(validated_execution.get("validated_inventory_complete", False)),
        "validated_runtime_matrix_expected_count": int(validated_execution.get("runtime_matrix_expected_count", 0)),
        "validated_runtime_matrix_passed_count": int(validated_execution.get("runtime_matrix_passed_count", 0)),
        "validated_clean_room_matrix_green": bool(validated_execution.get("runtime_matrix_green", False)),
        "validated_test_lane_expected_count": int(validated_execution.get("test_lane_expected_count", 0)),
        "validated_test_lane_passed_count": int(validated_execution.get("test_lane_passed_count", 0)),
        "validated_in_scope_test_lanes_green": bool(validated_execution.get("in_scope_test_lanes_green", False)),
        "migration_portability_passed": bool(validated_execution.get("migration_portability_passed", False)),
        "tier3_evidence_rebuilt_from_validated_runs": bool(validated_execution.get("tier3_evidence_rebuilt_from_validated_runs", False)),
        **bucket_counts,
    }
    certification_state = {
        "fully_certifiable_now": strict_independent_claims_ready and all_retained_tier3 and bool(artifact_truthfulness.get("passed", False)) and bool(validated_execution.get("runtime_matrix_green", False)) and bool(validated_execution.get("in_scope_test_lanes_green", False)) and bool(validated_execution.get("migration_portability_passed", False)) and bool(validated_execution.get("tier3_evidence_rebuilt_from_validated_runs", False)) and int(runtime_profile_report.get("summary", {}).get("ready_count", 0)) == len(runner_names) and int(runtime_profile_report.get("summary", {}).get("invalid_count", 0)) == 0 and int(runtime_profile_report.get("summary", {}).get("missing_count", 0)) == 0,
        "fully_rfc_compliant_now": strict_independent_claims_ready and all_protocol_tier3 and bool(validated_execution.get("runtime_matrix_green", False)) and bool(validated_execution.get("in_scope_test_lanes_green", False)) and bool(validated_execution.get("migration_portability_passed", False)),
        "protocol_boundary_tier3_complete": all_protocol_tier3,
        "retained_boundary_tier3_complete": all_retained_tier3,
        "strict_independent_claims_ready": strict_independent_claims_ready,
        "authoritative_scope_manifest": str(scope_path.relative_to(repo_root)) if scope_path.exists() else None,
        "boundary_freeze_active": bool(scope.get("boundary_freeze")),
        "boundary_freeze_passed": not scope_freeze_failures,
        "boundary_freeze_decision_id": str(scope.get("boundary_freeze", {}).get("decision_id", "")),
        "boundary_freeze_effective_date": str(scope.get("boundary_freeze", {}).get("effective_date", "")),
        "boundary_freeze_retained_target_count": int(scope.get("boundary_freeze", {}).get("retained_target_count", 0) or 0),
        "boundary_freeze_rfc_target_count": int(scope.get("boundary_freeze", {}).get("retained_rfc_target_count", 0) or 0),
        "boundary_freeze_non_rfc_target_count": int(scope.get("boundary_freeze", {}).get("retained_non_rfc_target_count", 0) or 0),
        "boundary_freeze_deferred_target_count": int(scope.get("boundary_freeze", {}).get("deferred_target_count", 0) or 0),
        "boundary_freeze_identity_hash_matches": bool(scope_freeze_summary.get("scope_freeze_retained_target_identity_hash_matches", False)),
        "clean_room_matrix_implemented": bool(current_state.get("tox_manifest_present", False) and current_state.get("install_profile_workflow_present", False) and current_state.get("release_gate_workflow_present", False)),
        "clean_room_matrix_executed_in_this_container": False,
        "tox_manifest_present": bool(current_state.get("tox_manifest_present", False)),
        "test_constraints_manifest_present": bool(current_state.get("test_constraints_manifest_present", False)),
        "tigrcorn_pin_committed": bool(current_state.get("tigrcorn_pin_committed", False)),
        "operator_plane_backend": str(current_state.get("operator_plane_backend", "unknown")),
        "operator_plane_repo_mutation_dependency": bool(current_state.get("operator_plane_repo_mutation_dependency", True)),
        "operator_plane_tenancy_enforced": bool(current_state.get("operator_plane_tenancy_enforced", False)),
        "tier4_supported_peer_profile_count": int(current_state.get("tier4_supported_peer_profile_count", 0)),
        "tier4_required_external_bundle_count": int(current_state.get("tier4_required_external_bundle_count", 0)),
        "tier4_external_bundle_count": int(current_state.get("tier4_external_bundle_count", 0)),
        "tier4_valid_external_bundle_count": int(current_state.get("tier4_valid_external_bundle_count", 0)),
        "tier4_invalid_external_bundle_count": int(current_state.get("tier4_invalid_external_bundle_count", 0)),
        "tier4_missing_external_bundle_count": int(current_state.get("tier4_missing_external_bundle_count", 0)),
        "tier4_peer_bundle_completeness_passed": bool(current_state.get("tier4_peer_bundle_completeness_passed", False)),
        "tier4_external_handoff_template_present": bool(current_state.get("tier4_external_handoff_template_present", False)),
        "tier3_ready_targets": sorted(str(entry.get("target")) for entry in claim_entries if int(entry.get("tier", 0)) >= 3),
        "tier4_ready_targets": sorted(str(entry.get("target")) for entry in claim_entries if int(entry.get("tier", 0)) >= 4),
        "validated_execution_artifact_count": int(validated_execution.get("validated_artifact_count", 0)),
        "required_validated_inventory_count": int(validated_execution.get("required_validated_inventory_count", 0)),
        "validated_inventory_present_count": int(validated_execution.get("validated_inventory_present_count", 0)),
        "validated_inventory_complete": bool(validated_execution.get("validated_inventory_complete", False)),
        "clean_room_matrix_green": bool(validated_execution.get("runtime_matrix_green", False)),
        "in_scope_test_lanes_green": bool(validated_execution.get("in_scope_test_lanes_green", False)),
        "migration_portability_passed": bool(validated_execution.get("migration_portability_passed", False)),
        "tier3_evidence_rebuilt_from_validated_runs": bool(validated_execution.get("tier3_evidence_rebuilt_from_validated_runs", False)),
        "open_gaps": [],
    }
    if not bool(current_state.get("boundary_freeze_passed", False)):
        certification_state["open_gaps"].append("The certification boundary freeze record is missing or inconsistent with the retained target set.")
    if not strict_independent_claims_ready:
        certification_state["open_gaps"].append("Tier 4 independent peer validation is not complete for the retained boundary.")
    if not all_retained_tier3:
        certification_state["open_gaps"].append("Some retained targets remain below Tier 3 and still require certification-grade closure.")
    if not bool(current_state.get("tier4_external_handoff_template_present", False)):
        certification_state["open_gaps"].append("The fill-in external handoff template package is not present for the full supported peer-profile set.")
    if int(current_state.get("tier4_missing_external_bundle_count", 0)) > 0:
        certification_state["open_gaps"].append("One or more supported peer profiles still have no preserved external Tier 4 bundle.")
    if not bool(current_state.get("tier4_peer_bundle_completeness_passed", False)):
        certification_state["open_gaps"].append("The peer-bundle completeness gate is not satisfied for the declared peer-profile set.")
    if int(current_state.get("tier4_invalid_external_bundle_count", 0)) > 0:
        certification_state["open_gaps"].append("One or more supported peer profiles have incomplete or invalid preserved external evidence bundles.")
    if bool(current_state.get("operator_plane_repo_mutation_dependency", True)):
        certification_state["open_gaps"].append("The certified resource administration workflow still depends on repository file mutation rather than a durable external control-plane backend.")
    if not bool(current_state.get("operator_plane_tenancy_enforced", False)):
        certification_state["open_gaps"].append("The storage-backed administration workflow does not yet enforce tenant scoping consistently across CRUD and portability workflows.")
    runtime_report_source_mode = str(runtime_profile_report.get("summary", {}).get("source_mode", runtime_profile_report.get("report_mode", "live-probe")))
    runtime_report_uses_validated_runs = runtime_report_source_mode == "validated-runs"
    if int(runtime_profile_report.get("summary", {}).get("invalid_count", 0)) > 0 or int(runtime_profile_report.get("summary", {}).get("missing_count", 0)) > 0:
        certification_state["open_gaps"].append(
            "The runtime validation stack now executes real app-factory, serve-check, and HTTP surface probes in the clean-room matrix, but successful execution across the supported interpreter/profile matrix is not yet preserved in the validated-run inventory."
            if runtime_report_uses_validated_runs
            else "The runtime validation stack now executes real app-factory, serve-check, and HTTP surface probes in the clean-room matrix, but successful execution across the supported interpreter/profile matrix is not preserved in this container."
        )
        certification_state["open_gaps"].append("Tigrcorn is now pinned and included in the clean-room matrix for Python 3.11/3.12, but preserved independent validation artifacts remain absent.")
    if int(runtime_profile_report.get("summary", {}).get("placeholder_supported_runner_count", 0)) > 0:
        certification_state["open_gaps"].append("At least one kept runner is still modeled as a placeholder rather than a published pinned package.")
    if not bool(runtime_profile_report.get("summary", {}).get("declared_ci_install_probe_complete", False)):
        certification_state["open_gaps"].append("At least one kept runner is missing declared clean-room CI install/probe coverage.")
    if not bool(runtime_profile_report.get("summary", {}).get("surface_probe_passed", False)):
        certification_state["open_gaps"].append(
            "The runtime HTTP surface probe is not yet proven green across the preserved validated base-environment manifests."
            if runtime_report_uses_validated_runs
            else "The runtime HTTP surface probe did not pass in the current environment."
        )
    if not bool(runtime_profile_report.get("application_probe", {}).get("passed", False)):
        certification_state["open_gaps"].append(
            "The application factory is not yet proven materialized across the preserved validated base-environment manifests."
            if runtime_report_uses_validated_runs
            else "The application factory did not materialize in the current environment, so runtime validation could not complete here."
        )
    if not bool(runtime_profile_report.get("summary", {}).get("execution_probe_complete", False)):
        certification_state["open_gaps"].append(
            "Real runtime execution probes are implemented in tox and CI, but the preserved validated runtime inventory does not yet cover the full kept-runner matrix."
            if runtime_report_uses_validated_runs
            else "Real runtime execution probes are implemented in tox and CI, but the full kept-runner probe set was not executed successfully in this container."
        )
    if not bool(validated_execution.get("runtime_matrix_green", False)):
        certification_state["open_gaps"].append("Validated clean-room install matrix evidence is incomplete or missing.")
    if not bool(validated_execution.get("in_scope_test_lanes_green", False)):
        certification_state["open_gaps"].append("Validated in-scope certification lane execution evidence is incomplete or missing.")
    if not bool(validated_execution.get("migration_portability_passed", False)):
        certification_state["open_gaps"].append("Migration upgrade → downgrade → reapply portability has not been preserved for both SQLite and PostgreSQL.")
    if not bool(validated_execution.get("tier3_evidence_rebuilt_from_validated_runs", False)):
        certification_state["open_gaps"].append("Tier 3 evidence has not yet been explicitly rebuilt from validated-run manifests.")
    if not artifact_truthfulness.get("passed", False):
        certification_state["open_gaps"].append("Current generated public artifacts still drift from executable reality.")
    if not bool(current_state.get("fully_featured_package_boundary_now", False)):
        certification_state["open_gaps"].append("One or more exported package capabilities still lacks end-to-end verification in the current environment.")
    if not bool(current_state.get("certification_evidence_index_passed", False)):
        certification_state["open_gaps"].append("At least one claim row is still missing a machine-derived certification proof binding.")
    if not bool(current_state.get("release_evidence_clean_checkout_now", False)):
        certification_state["open_gaps"].append("Release evidence can now be built only from a clean checkout, and the current workspace is dirty.")
    if not bool(current_state.get("feature_release_verify_verb_present", False)):
        certification_state["open_gaps"].append("The CLI release surface is still missing an explicit verify verb for signed bundle verification.")
    if int(artifact_truthfulness.get("summary", {}).get("authoritative_current_doc_stale_ref_count", 0)) > 0:
        certification_state["open_gaps"].append("Current authoritative docs still contain stale code-path references.")
    report_dir = repo_root / "docs" / "compliance"
    _write_report(
        report_dir,
        "current_state_report",
        {"passed": True, "summary": current_state, "details": {"targets": ", ".join(targets)}},
        "Current State Report",
    )
    _write_report(
        report_dir,
        "certification_state_report",
        {"passed": bool(certification_state["fully_certifiable_now"] and certification_state["fully_rfc_compliant_now"] and certification_state["strict_independent_claims_ready"]), "summary": certification_state, "details": certification_state["open_gaps"]},
        "Certification State Report",
    )
    return {"current_state": current_state, "certification_state": certification_state}



EXPECTED_PYTHON_VERSIONS = ["3.10", "3.11", "3.12"]
EXPECTED_TIGRCORN_PYTHON_VERSIONS = ["3.11", "3.12"]
EXPECTED_RUNTIME_VALIDATION_MATRIX = {
    "base": EXPECTED_PYTHON_VERSIONS,
    "sqlite-uvicorn": EXPECTED_PYTHON_VERSIONS,
    "postgres-hypercorn": EXPECTED_PYTHON_VERSIONS,
    "tigrcorn": EXPECTED_TIGRCORN_PYTHON_VERSIONS,
    "devtest": EXPECTED_PYTHON_VERSIONS,
}
