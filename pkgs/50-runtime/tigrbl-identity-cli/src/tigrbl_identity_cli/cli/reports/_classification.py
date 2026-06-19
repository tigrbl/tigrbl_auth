from __future__ import annotations

def verify_peer_bundle_completeness(repo_root: Path, *, strict: bool = True) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    profile_dir = repo_root / "compliance" / "evidence" / "peer_profiles"
    bundle_dir = repo_root / "compliance" / "evidence" / "tier4" / "bundles"
    declared_profiles = sorted(path.stem for path in profile_dir.glob("*.yaml"))
    bundle_rows: dict[str, dict[str, Any]] = {}
    invalid_profiles: list[str] = []
    invalid_bundle_dirs: list[str] = []

    for path in sorted(bundle_dir.iterdir()) if bundle_dir.exists() else []:
        if not path.is_dir():
            continue
        manifest_path = path / "manifest.yaml"
        if not manifest_path.exists():
            continue
        manifest = _load_yaml(manifest_path) or {}
        profile = str(manifest.get("peer_profile", "")).strip()
        if not profile:
            invalid_bundle_dirs.append(str(path.relative_to(repo_root)))
            continue
        qualifies, bundle_failures, details = evaluate_tier4_bundle(path, manifest)
        bundle_rows[profile] = {
            "bundle_dir": str(path.relative_to(repo_root)),
            "status": details["status"],
            "attestation_class": details["attestation_class"],
            "peer_operator": details["peer_operator"],
            "peer_version": details["peer_version"],
            "scenario_result_count": len(list(manifest.get("scenario_results") or [])),
            "has_reproduction": details["has_reproduction"],
            "validation_failure_count": details["validation_failure_count"],
            "qualifies_for_promotion": qualifies,
            "qualification_failures": bundle_failures,
        }
        if not qualifies:
            invalid_profiles.append(profile)

    missing_profiles = [profile for profile in declared_profiles if profile not in bundle_rows]
    failures = [f"Missing preserved external bundle for declared peer profile: {profile}" for profile in missing_profiles]
    failures.extend(f"Invalid preserved bundle manifest missing peer_profile: {path}" for path in invalid_bundle_dirs)
    failures.extend(f"Preserved external bundle is present but not promotion-qualifying: {profile}" for profile in sorted(invalid_profiles))
    payload = {
        "passed": not failures,
        "failures": failures,
        "warnings": [],
        "summary": {
            "declared_peer_profile_count": len(declared_profiles),
            "preserved_bundle_count": len(bundle_rows),
            "valid_bundle_count": len(bundle_rows) - len(invalid_profiles),
            "invalid_bundle_count": len(invalid_profiles),
            "missing_bundle_count": len(missing_profiles),
            "missing_profiles": missing_profiles,
            "invalid_profiles": sorted(invalid_profiles),
            "bundle_dir": str(bundle_dir.relative_to(repo_root)),
        },
        "details": [
            {
                "profile": profile,
                "bundle_present": profile in bundle_rows,
                **(bundle_rows.get(profile) or {}),
            }
            for profile in declared_profiles
        ],
    }
    _write_report(
        repo_root / "docs" / "compliance",
        "peer_bundle_completeness_report",
        payload,
        "Peer Bundle Completeness Report",
    )
    return payload


GATE_CALLS = {
    "gate-00-structure": lambda root: run_governance_install_check(root, strict=True),
    "gate-05-governance": lambda root: run_governance_install_check(root, strict=True),
    "gate-08-claim-registry-sync": lambda root: 0 if verify_claim_registries(root)["passed"] else 1,
    "gate-10-static": lambda root: run_runtime_foundation_check(root, strict=True),
    "gate-12-project-tree-layout": lambda root: run_project_tree_layout_check(root, strict=True),
    "gate-15-boundary-enforcement": lambda root: run_boundary_enforcement_check(root, strict=True),
    "gate-18-migration-plan": lambda root: run_migration_plan_check(root, strict=True),
    "gate-19-package-maturity": lambda root: 0 if evaluate_package_maturity(root, target_tier="T2")["passed"] else 1,
    "gate-20-tests": lambda root: 0 if run_test_execution_gate(root)["passed"] else 1,
    "gate-25-wrapper-hygiene": lambda root: run_wrapper_hygiene_check(root, strict=True),
    "gate-30-contracts": lambda root: 0 if validate_openapi_contract(root).passed and validate_openrpc_contract(root).passed else 1,
    "gate-35-contract-sync": lambda root: run_contract_sync_check(root, strict=True),
    "gate-40-evidence": lambda root: 0 if summarize_evidence_status(root)["passed"] else 1,
    "gate-45-evidence-peer": lambda root: run_evidence_peer_check(root, strict=True),
    "gate-50-release-bundle": lambda root: 0 if build_release_bundle(root, deployment_from_options()).exists() else 1,
    "gate-55-contract-validation": lambda root: 0 if validate_openapi_contract(root).passed and validate_openrpc_contract(root).passed else 1,
    "gate-60-release-signing": lambda root: _run_release_signing_gate(root),
    "gate-65-state-reports": lambda root: 0 if generate_state_reports(root) else 1,
    "gate-75-test-classification": lambda root: 0 if verify_test_classification(root, strict=True)["passed"] else 1,
    "gate-85-peer-profiles": lambda root: 0 if execute_peer_profiles(root, deployment_from_options(profile="hardening"), execution_mode="self-check")["passed"] else 1,
    "gate-87-peer-bundle-completeness": lambda root: 0 if verify_peer_bundle_completeness(root, strict=True)["passed"] else 1,
    "gate-90-release": lambda root: 0 if run_final_release_readiness_gate(root)["passed"] else 1,
    "gate-truth-current-state": lambda root: 0 if verify_truth_chain(root, mode="current-state")["passed"] else 1,
    "gate-truth-release-decision": lambda root: 0 if verify_truth_chain(root, mode="release-decision")["passed"] else 1,
    "gate-truth-repository-state": lambda root: 0 if verify_truth_chain(root, mode="repository-state")["passed"] else 1,
    "gate-95-recertification": lambda root: 0 if run_recertification(root)["passed"] else 1,
}


def _build_release_gate_payload(repo_root: Path, gate_names: list[str], results: list[dict[str, Any]], failures: list[str]) -> dict[str, Any]:
    validated = load_validated_execution_status(repo_root)
    return {
        "passed": not failures,
        "failures": failures,
        "warnings": [],
        "summary": {
            "gate_count": len(gate_names),
            "failed_gate_count": len([item for item in results if not item["passed"]]),
            "validated_execution_artifact_count": int(validated.get("validated_artifact_count", 0)),
            "required_validated_inventory_count": int(validated.get("required_validated_inventory_count", 0)),
            "validated_inventory_present_count": int(validated.get("validated_inventory_present_count", 0)),
            "validated_inventory_complete": bool(validated.get("validated_inventory_complete", False)),
            "clean_room_install_matrix_green": bool(validated.get("runtime_matrix_green", False)),
            "in_scope_test_lanes_green": bool(validated.get("in_scope_test_lanes_green", False)),
            "migration_portability_passed": bool(validated.get("migration_portability_passed", False)),
            "tier3_evidence_rebuilt_from_validated_runs": bool(validated.get("tier3_evidence_rebuilt_from_validated_runs", False)),
        },
        "details": results,
    }


TIER4_ONLY_GATES = {"gate-45-evidence-peer", "gate-87-peer-bundle-completeness"}


def _repository_tier(repo_root: Path) -> int:
    scope = _load_yaml(repo_root / "compliance" / "targets" / "certification_scope.yaml")
    try:
        return int(scope.get("repository_tier", 0))
    except (TypeError, ValueError):
        return 0


def run_release_gates(repo_root: Path, *, gate_name: str | None = None, strict: bool = True) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    _ensure_repo_local_operator_state(repo_root)
    repository_tier = _repository_tier(repo_root)
    gate_dir = repo_root / "compliance" / "gates"
    ordered = _load_yaml(gate_dir / "gate-order.yaml") if (gate_dir / "gate-order.yaml").exists() else {"ordered_gates": sorted(GATE_CALLS)}
    gate_names = [gate_name] if gate_name and gate_name not in {"all", "*"} else list(ordered.get("ordered_gates", sorted(GATE_CALLS)))
    truth_gate_names = [name for name in gate_names if name.startswith("gate-truth-")]
    primary_gate_names = [name for name in gate_names if name not in truth_gate_names]

    primary_results: list[dict[str, Any]] = []
    primary_failures: list[str] = []
    for name in primary_gate_names:
        fn = GATE_CALLS.get(name)
        if fn is None:
            primary_failures.append(f"Unknown gate: {name}")
            continue
        try:
            rc = int(fn(repo_root))
            error: str | None = None
        except Exception as exc:
            rc = 1
            error = str(exc)
        non_blocking_tier4_gate = name in TIER4_ONLY_GATES and repository_tier < 4
        passed = rc == 0 or non_blocking_tier4_gate
        result = {"gate": name, "passed": passed, "rc": 0 if non_blocking_tier4_gate else rc}
        if non_blocking_tier4_gate:
            result["observed_rc"] = rc
            result["non_blocking"] = True
            result["reason"] = f"repository_tier={repository_tier}; Tier 4 peer promotion is recorded but not release-blocking"
        if error:
            result["error"] = error
        primary_results.append(result)
        if not passed:
            primary_failures.append(f"Gate failed: {name}" + (f" ({error})" if error else ""))

    payload = _build_release_gate_payload(repo_root, primary_gate_names, primary_results, primary_failures)
    _write_report(repo_root / "docs" / "compliance", "release_gate_report", payload, "Release Gate Report")
    materialize_truth_chain(repo_root)

    if not truth_gate_names:
        return payload

    def _run_truth_pass() -> tuple[list[dict[str, Any]], list[str]]:
        truth_results: list[dict[str, Any]] = []
        truth_failures: list[str] = []
        for name in truth_gate_names:
            fn = GATE_CALLS.get(name)
            if fn is None:
                truth_failures.append(f"Unknown gate: {name}")
                continue
            try:
                rc = int(fn(repo_root))
                error: str | None = None
            except Exception as exc:
                rc = 1
                error = str(exc)
            passed = rc == 0
            result = {"gate": name, "passed": passed, "rc": rc}
            if error:
                result["error"] = error
            truth_results.append(result)
            if not passed:
                truth_failures.append(f"Gate failed: {name}" + (f" ({error})" if error else ""))
        return truth_results, truth_failures

    truth_results, truth_failures = _run_truth_pass()
    combined_results = primary_results + truth_results
    combined_failures = primary_failures + truth_failures
    payload = _build_release_gate_payload(repo_root, gate_names, combined_results, combined_failures)
    _write_report(repo_root / "docs" / "compliance", "release_gate_report", payload, "Release Gate Report")
    materialize_truth_chain(repo_root)

    truth_results, truth_failures = _run_truth_pass()
    combined_results = primary_results + truth_results
    combined_failures = primary_failures + truth_failures
    payload = _build_release_gate_payload(repo_root, gate_names, combined_results, combined_failures)
    _write_report(repo_root / "docs" / "compliance", "release_gate_report", payload, "Release Gate Report")
    materialize_truth_chain(repo_root)
    return payload


def build_release_bundle(
    repo_root: Path,
    deployment: Any,
    *,
    bundle_dir: Path | None = None,
    artifact: str = "all",
    require_clean_checkout: bool = False,
) -> Path:
    repo_root = repo_root.resolve()
    clean_checkout = _git_checkout_summary(repo_root)
    if require_clean_checkout and not bool(clean_checkout.get("clean", False)):
        changed = ", ".join(clean_checkout.get("changed_paths", [])[:10]) or "unknown paths"
        raise RuntimeError(f"release evidence requires a clean checkout; dirty paths detected: {changed}")
    version = _current_version(repo_root)
    bundle_root = bundle_dir or (repo_root / "dist" / "release-bundles" / version / deployment.profile)
    if bundle_root.exists():
        shutil.rmtree(bundle_root)
    bundle_root.mkdir(parents=True, exist_ok=True)
    build_evidence_bundle(repo_root, deployment, tier="3", profile_label=deployment.profile, bundle_dir=bundle_root / "evidence")
    copied: list[dict[str, Any]] = []
    if artifact in {"claims", "all"}:
        copied.append(_copy_rel_artifact(repo_root, f"compliance/claims/effective-target-claims.{deployment.profile}.yaml", bundle_root))
    if artifact in {"evidence", "all"}:
        copied.append(_copy_rel_artifact(repo_root, f"compliance/evidence/effective-release-evidence.{deployment.profile}.yaml", bundle_root))
    if artifact in {"contracts", "all"}:
        copied.append(_copy_rel_artifact(repo_root, str(_openapi_path(repo_root, deployment.profile).relative_to(repo_root)), bundle_root))
        copied.append(_copy_rel_artifact(repo_root, str(_openrpc_path(repo_root, deployment.profile).relative_to(repo_root)), bundle_root))
    for rel_path in _dependency_artifact_paths(repo_root):
        copied.append(_copy_rel_artifact(repo_root, rel_path, bundle_root))
    write_authoritative_current_docs_manifest(repo_root)
    authority = load_document_authority(repo_root)
    generated_doc_paths = list(dict.fromkeys(_docs_for_certification_bundle(repo_root)))
    supporting_non_doc_paths = list(dict.fromkeys(authority.get("supporting_current_non_doc_artifacts", [])))
    for rel_path in generated_doc_paths + supporting_non_doc_paths:
        if (repo_root / rel_path).exists():
            copied.append(_copy_rel_artifact(repo_root, rel_path, bundle_root))
    discovery_dir = repo_root / "specs" / "discovery" / "profiles" / deployment.profile
    if discovery_dir.exists():
        for path in sorted(discovery_dir.glob("*.json")):
            copied.append(_copy_rel_artifact(repo_root, str(path.relative_to(repo_root)), bundle_root))
    peer_dir = repo_root / "compliance" / "evidence" / "tier4" / "executions"
    for path in sorted(peer_dir.glob(f"*.{deployment.profile}.yaml")):
        copied.append(_copy_rel_artifact(repo_root, str(path.relative_to(repo_root)), bundle_root))
    current_report = _load_json_if_exists(repo_root / "docs" / "compliance" / "current_state_report.json") or {}
    cert_report = _load_json_if_exists(repo_root / "docs" / "compliance" / "certification_state_report.json") or {}
    gate_report = _load_json_if_exists(repo_root / "docs" / "compliance" / "release_gate_report.json") or {}
    final_gate_report = _load_json_if_exists(repo_root / "docs" / "compliance" / "final_release_gate_report.json") or {}
    validated_report = _load_json_if_exists(repo_root / "docs" / "compliance" / "validated_execution_report.json") or {}
    final_release_status = _load_json_if_exists(repo_root / "docs" / "compliance" / "FINAL_RELEASE_STATUS_2026-03-25.json") or {}
    cert_summary = cert_report.get("summary", {}) if isinstance(cert_report, dict) else {}
    manifest = {
        "schema_version": 1,
        "package": "tigrbl_auth",
        "version": version,
        "profile": deployment.profile,
        "artifact_selection": artifact,
        "deployment": deployment.to_manifest(),
        "dependency_provenance": {
            "artifact_paths": _dependency_artifact_paths(repo_root),
            "native_uv_lock_present": (repo_root / "uv.lock").exists(),
            "equivalent_lock_manifest": "constraints/dependency-lock.json" if (repo_root / "constraints" / "dependency-lock.json").exists() else None,
        },
        "documentation_scope": {
            "generated_current_state_docs_only": True,
            "authoritative_current_docs_spec": authority.get("path"),
            "document_authority_projection_manifest": authority.get("projection_path"),
            "authoritative_current_docs_manifest": "docs/compliance/AUTHORITATIVE_CURRENT_DOCS.json",
            "copied_generated_doc_paths": generated_doc_paths,
            "copied_supporting_non_doc_paths": supporting_non_doc_paths,
            "historical_archive_root": "docs/archive/historical",
        },
        "release_classification": (
            "final-certification-release"
            if bool(cert_summary.get("fully_certifiable_now", False))
            and bool(cert_summary.get("fully_rfc_compliant_now", False))
            and bool(cert_summary.get("strict_independent_claims_ready", False))
            and bool(final_gate_report.get("passed", False))
            else "candidate-checkpoint-not-certified"
        ),
        "current_state_summary": current_report.get("summary", {}) if isinstance(current_report, dict) else {},
        "certification_state_summary": cert_summary,
        "release_gate_summary": gate_report.get("summary", {}) if isinstance(gate_report, dict) else {},
        "final_release_gate_summary": final_gate_report.get("summary", {}) if isinstance(final_gate_report, dict) else {},
        "final_release_status": final_release_status.get("summary", {}) if isinstance(final_release_status, dict) else {},
        "validated_execution_summary": validated_report.get("summary", {}) if isinstance(validated_report, dict) else {},
        "clean_checkout_required": bool(require_clean_checkout),
        "clean_checkout": clean_checkout,
        "artifacts": copied,
    }
    _write_json(bundle_root / "release-bundle.json", manifest)
    _write_yaml(bundle_root / "release-bundle.yaml", manifest)
    digests = {item["path"]: item.get("sha256") for item in copied if item.get("present") and item.get("sha256")}
    _write_json(bundle_root / "digests.json", digests)
    return bundle_root


def _artifact_media_type(rel_path: str) -> str:
    if rel_path.endswith(".json"):
        return "application/json"
    if rel_path.endswith(".yaml") or rel_path.endswith(".yml"):
        return "application/yaml"
    return "application/octet-stream"
