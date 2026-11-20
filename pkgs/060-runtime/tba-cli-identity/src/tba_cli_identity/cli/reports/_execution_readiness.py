from __future__ import annotations


def run_final_release_readiness_gate(repo_root: Path) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    _ensure_repo_local_operator_state(repo_root)
    generate_state_reports(repo_root)
    validated = load_validated_execution_status(repo_root)
    runtime_profile_path = repo_root / "docs" / "compliance" / "runtime_profile_report.json"
    certification_state_path = repo_root / "docs" / "compliance" / "certification_state_report.json"
    runtime_profile = json.loads(runtime_profile_path.read_text(encoding="utf-8")) if runtime_profile_path.exists() else {}
    certification_state = json.loads(certification_state_path.read_text(encoding="utf-8")) if certification_state_path.exists() else {}
    runner_count = len(registered_runner_names())
    summary = runtime_profile.get("summary", {}) if isinstance(runtime_profile, dict) else {}
    failures: list[str] = []
    runtime_report_source_mode = str(summary.get("source_mode", runtime_profile.get("report_mode", "live-probe")))
    if int(summary.get("ready_count", 0)) != runner_count:
        failures.append(
            "Runtime profiles are not all ready in the preserved validated-run inventory."
            if runtime_report_source_mode == "validated-runs"
            else "Runtime profiles are not all ready in the current certification environment."
        )
    if int(summary.get("invalid_count", 0)) != 0:
        failures.append("At least one kept runner is still invalid.")
    if int(summary.get("missing_count", 0)) != 0:
        failures.append("At least one kept runner is still missing.")
    if not validated.get("validated_inventory_complete", False):
        failures.append(
            "Validated artifact inventory is below the required "
            f"{validated.get('required_validated_inventory_count', 0)} artifact threshold."
        )
    if not validated.get("runtime_matrix_green", False):
        failures.append("The clean-room install matrix is not green from validated-run evidence.")
    if not validated.get("in_scope_test_lanes_green", False):
        failures.append("In-scope certification test lanes are not green from validated-run evidence.")
    if not validated.get("migration_portability_passed", False):
        failures.append("Migration portability validation is not preserved for both SQLite and PostgreSQL.")
    if not validated.get("tier3_evidence_rebuilt_from_validated_runs", False):
        failures.append("Tier 3 evidence has not been rebuilt from validated runs.")
    tier4_ready = bool(certification_state.get("summary", {}).get("strict_independent_claims_ready", False))
    warnings: list[str] = []
    if not tier4_ready:
        warnings.append("Tier 4 bundle promotion is not complete for the retained boundary.")
    payload = {
        "passed": not failures,
        "failures": failures,
        "warnings": warnings,
        "summary": {
            "runtime_profiles_truly_ready": int(summary.get("ready_count", 0)) == runner_count and int(summary.get("invalid_count", 0)) == 0 and int(summary.get("missing_count", 0)) == 0,
            "validated_inventory_complete": bool(validated.get("validated_inventory_complete", False)),
            "required_validated_inventory_count": int(validated.get("required_validated_inventory_count", 0)),
            "validated_inventory_present_count": int(validated.get("validated_inventory_present_count", 0)),
            "clean_room_install_matrix_green": bool(validated.get("runtime_matrix_green", False)),
            "in_scope_test_lanes_green": bool(validated.get("in_scope_test_lanes_green", False)),
            "migration_portability_passed": bool(validated.get("migration_portability_passed", False)),
            "tier3_evidence_rebuilt_from_validated_runs": bool(validated.get("tier3_evidence_rebuilt_from_validated_runs", False)),
            "tier4_bundle_promotion_complete": tier4_ready,
        },
    }
    _write_report(repo_root / "docs" / "compliance", "final_release_gate_report", payload, "Final Release Gate Report")
    return payload
