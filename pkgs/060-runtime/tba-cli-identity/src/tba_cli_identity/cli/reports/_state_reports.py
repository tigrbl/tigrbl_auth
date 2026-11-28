from __future__ import annotations

EXPECTED_TEST_LANE_MATRIX = {
    "core": EXPECTED_PYTHON_VERSIONS,
    "integration": EXPECTED_PYTHON_VERSIONS,
    "conformance": EXPECTED_PYTHON_VERSIONS,
    "security-negative": EXPECTED_PYTHON_VERSIONS,
    "interop": EXPECTED_PYTHON_VERSIONS,
}


def _runtime_manifest_counts_as_passed(payload: dict[str, Any]) -> bool:
    return validated_runtime_manifest_passed(payload)


def _coerce_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _test_lane_manifest_counts_as_passed(payload: dict[str, Any]) -> bool:
    return validated_test_lane_manifest_passed(payload)



def _tier3_evidence_manifest_counts_as_passed(payload: dict[str, Any]) -> bool:
    return bool(
        payload.get("passed", False)
        and payload.get("rebuild_from_validated_runs_only", False)
        and payload.get("runtime_report_generated_from_validated_runs", False)
        and payload.get("validated_execution_report_present", False)
        and payload.get("runtime_profile_report_present", False)
        and (_coerce_int(payload.get("recognized_manifest_count")) or 0) > 0
    )



def load_validated_execution_status(repo_root: Path) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    validated_root = repo_root / "dist" / "validated-runs"
    manifests: list[dict[str, Any]] = []
    ignored_json_paths: list[str] = []
    if validated_root.exists():
        for path in sorted(validated_root.rglob("*.json")):
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                ignored_json_paths.append(str(path.relative_to(repo_root)))
                continue
            if isinstance(payload, dict):
                payload["_path"] = str(path.relative_to(repo_root))
                manifests.append(payload)
            else:
                ignored_json_paths.append(str(path.relative_to(repo_root)))

    required_runtime = [(profile, version) for profile, versions in EXPECTED_RUNTIME_VALIDATION_MATRIX.items() for version in versions]
    required_runtime_keys = set(required_runtime)
    required_lanes = [(lane, version) for lane, versions in EXPECTED_TEST_LANE_MATRIX.items() for version in versions]
    required_lane_keys = set(required_lanes)

    runtime_manifests: dict[tuple[str, str], dict[str, Any]] = {}
    lane_manifests: dict[tuple[str, str], dict[str, Any]] = {}
    migration_manifests: list[dict[str, Any]] = []
    migration_backend_manifests: dict[str, list[dict[str, Any]]] = {}
    tier3_evidence_manifests: list[dict[str, Any]] = []
    recognized_manifests: list[dict[str, Any]] = []
    in_scope_manifests: list[dict[str, Any]] = []
    out_of_scope_manifests: list[dict[str, Any]] = []

    def _record_out_of_scope(item: dict[str, Any], *, identity: str, reason: str) -> None:
        out_of_scope_manifests.append(
            {
                "path": item.get("_path"),
                "kind": item.get("kind"),
                "python_version": item.get("python_version"),
                "identity": identity,
                "reason": reason,
            }
        )

    for payload in manifests:
        kind = str(payload.get("kind", ""))
        pyver = str(payload.get("python_version", ""))
        if kind == "runtime-profile":
            profile = str(payload.get("matrix_profile", "unknown"))
            key = (profile, pyver)
            runtime_manifests[key] = payload
            recognized_manifests.append(payload)
            if key in required_runtime_keys:
                in_scope_manifests.append(payload)
            else:
                _record_out_of_scope(payload, identity=f"{profile}@py{pyver}", reason="runtime profile is outside the supported certification matrix")
        elif kind == "test-lane":
            lane = str(payload.get("lane", "unknown"))
            key = (lane, pyver)
            lane_manifests[key] = payload
            recognized_manifests.append(payload)
            if key in required_lane_keys:
                in_scope_manifests.append(payload)
            else:
                _record_out_of_scope(payload, identity=f"{lane}@py{pyver}", reason="test lane is outside the supported certification matrix")
        elif kind == "migration-portability":
            migration_manifests.append(payload)
            recognized_manifests.append(payload)
        elif kind == "migration-portability-backend":
            backend = str(payload.get("backend", "unknown"))
            migration_backend_manifests.setdefault(backend, []).append(payload)
            recognized_manifests.append(payload)
            in_scope_manifests.append(payload)
        elif kind == "tier3-evidence":
            tier3_evidence_manifests.append(payload)
            recognized_manifests.append(payload)
            in_scope_manifests.append(payload)
        else:
            ignored_json_paths.append(str(payload.get("_path", "")))

    passed_runtime = [
        f"{profile}@py{version}"
        for profile, version in required_runtime
        if _runtime_manifest_counts_as_passed(runtime_manifests.get((profile, version), {}))
    ]
    missing_runtime = [
        f"{profile}@py{version}"
        for profile, version in required_runtime
        if not _runtime_manifest_counts_as_passed(runtime_manifests.get((profile, version), {}))
    ]

    passed_lanes = [
        f"{lane}@py{version}"
        for lane, version in required_lanes
        if _test_lane_manifest_counts_as_passed(lane_manifests.get((lane, version), {}))
    ]
    missing_lanes = [
        f"{lane}@py{version}"
        for lane, version in required_lanes
        if not _test_lane_manifest_counts_as_passed(lane_manifests.get((lane, version), {}))
    ]

    runtime_present_count = sum(1 for profile, version in required_runtime if (profile, version) in runtime_manifests)
    lane_present_count = sum(1 for lane, version in required_lanes if (lane, version) in lane_manifests)
    required_migration_backends = ("sqlite", "postgres")
    migration_manifest_present = bool(migration_manifests) and all(
        backend in migration_backend_manifests for backend in required_migration_backends
    )

    def _migration_backend_group_passed(backend: str) -> bool:
        return any(
            validated_migration_backend_manifest_passed(item)
            for item in migration_backend_manifests.get(backend, [])
        )

    migration_portability_passed = bool(
        any(validated_migration_manifest_passed(item) for item in migration_manifests)
        and all(_migration_backend_group_passed(backend) for backend in required_migration_backends)
    )
    tier3_evidence_rebuilt_from_validated_runs = any(_tier3_evidence_manifest_counts_as_passed(item) for item in tier3_evidence_manifests)
    required_validated_inventory_count = len(required_runtime) + len(required_lanes) + len(required_migration_backends)
    validated_inventory_present_count = runtime_present_count + lane_present_count + sum(
        1 for backend in required_migration_backends if backend in migration_backend_manifests
    )
    validated_inventory_complete = validated_inventory_present_count >= required_validated_inventory_count

    payload = {
        "validated_artifact_count": len(in_scope_manifests),
        "out_of_scope_validated_artifact_count": len(out_of_scope_manifests),
        "required_validated_inventory_count": required_validated_inventory_count,
        "validated_inventory_present_count": validated_inventory_present_count,
        "validated_inventory_complete": validated_inventory_complete,
        "runtime_matrix_present_count": runtime_present_count,
        "test_lane_present_count": lane_present_count,
        "migration_manifest_present": migration_manifest_present,
        "runtime_matrix_expected_count": len(required_runtime),
        "runtime_matrix_passed_count": len(passed_runtime),
        "runtime_matrix_green": len(missing_runtime) == 0,
        "runtime_matrix_missing": missing_runtime,
        "runtime_matrix_passed": passed_runtime,
        "test_lane_expected_count": len(required_lanes),
        "test_lane_passed_count": len(passed_lanes),
        "in_scope_test_lanes_green": len(missing_lanes) == 0,
        "test_lane_missing": missing_lanes,
        "test_lane_passed": passed_lanes,
        "migration_portability_passed": migration_portability_passed,
        "tier3_evidence_rebuilt_from_validated_runs": tier3_evidence_rebuilt_from_validated_runs,
        "tier3_evidence_manifest_count": len(tier3_evidence_manifests),
        "validated_root_present": validated_root.exists(),
        "ignored_json_paths": ignored_json_paths,
        "out_of_scope_validated_manifests": out_of_scope_manifests,
    }
    inventory_threshold_text = (
        f"{len(required_runtime)} runtime + {len(required_lanes)} test lanes "
        f"+ {len(required_migration_backends)} backend-distinct migration threshold"
    )
    report = {
        "passed": payload["runtime_matrix_green"] and payload["in_scope_test_lanes_green"] and payload["migration_portability_passed"],
        "failures": [
            *([f"Validated artifact inventory is below the required {inventory_threshold_text}."] if not payload["validated_inventory_complete"] else []),
            *(["Validated clean-room runtime matrix is incomplete."] if not payload["runtime_matrix_green"] else []),
            *(["Validated in-scope certification lane execution is incomplete."] if not payload["in_scope_test_lanes_green"] else []),
            *(["Migration portability validation across SQLite and PostgreSQL is missing."] if not payload["migration_portability_passed"] else []),
        ],
        "warnings": [
            "Tier 3 evidence has not yet been explicitly rebuilt from validated-run manifests."
            if not payload["tier3_evidence_rebuilt_from_validated_runs"]
            else "",
            "Unsupported-version or out-of-scope validated manifests are present and excluded from certification counts."
            if out_of_scope_manifests
            else "",
        ],
        "summary": {
            "validated_artifact_count": payload["validated_artifact_count"],
            "out_of_scope_validated_artifact_count": payload["out_of_scope_validated_artifact_count"],
            "required_validated_inventory_count": payload["required_validated_inventory_count"],
            "validated_inventory_present_count": payload["validated_inventory_present_count"],
            "validated_inventory_complete": payload["validated_inventory_complete"],
            "runtime_matrix_present_count": payload["runtime_matrix_present_count"],
            "runtime_matrix_expected_count": payload["runtime_matrix_expected_count"],
            "runtime_matrix_passed_count": payload["runtime_matrix_passed_count"],
            "runtime_matrix_green": payload["runtime_matrix_green"],
            "test_lane_expected_count": payload["test_lane_expected_count"],
            "test_lane_passed_count": payload["test_lane_passed_count"],
            "in_scope_test_lanes_green": payload["in_scope_test_lanes_green"],
            "migration_portability_passed": payload["migration_portability_passed"],
            "tier3_evidence_rebuilt_from_validated_runs": payload["tier3_evidence_rebuilt_from_validated_runs"],
        },
        "details": {
            "runtime_matrix_missing": payload["runtime_matrix_missing"],
            "runtime_matrix_present_count": payload["runtime_matrix_present_count"],
            "test_lane_missing": payload["test_lane_missing"],
            "test_lane_present_count": payload["test_lane_present_count"],
            "migration_manifest_present": payload["migration_manifest_present"],
            "required_validated_inventory_count": payload["required_validated_inventory_count"],
            "validated_inventory_present_count": payload["validated_inventory_present_count"],
            "validated_inventory_complete": payload["validated_inventory_complete"],
            "runtime_evidence": {
                f"{profile}@py{version}": {
                    "path": item.get("_path"),
                    "manifest_passed": bool(item.get("passed", False)),
                    "counts_as_passed": _runtime_manifest_counts_as_passed(item),
                    "identity": item.get("identity"),
                    "environment_identity_ready": environment_identity_ready(item),
                    "install_evidence_ready": install_evidence_ready(item),
                    "runtime_smoke_passed": bool(item.get("runtime_smoke_passed", False)),
                    "application_probe_passed": bool(item.get("application_probe_passed", False)),
                    "surface_probe_passed": bool(item.get("surface_probe_passed", False)),
                    "runner_available": item.get("runner_available"),
                    "serve_check_passed": item.get("serve_check_passed"),
                }
                for (profile, version), item in sorted(runtime_manifests.items())
            },
            "test_lane_evidence": {
                f"{lane}@py{version}": {
                    "path": item.get("_path"),
                    "manifest_passed": bool(item.get("passed", False)),
                    "counts_as_passed": _test_lane_manifest_counts_as_passed(item),
                    "identity": item.get("identity"),
                    "environment_identity_ready": environment_identity_ready(item),
                    "install_evidence_ready": install_evidence_ready(item),
                    "pytest_report_present": bool(item.get("pytest_report_present", False) or item.get("pytest_report_artifact")),
                    "pytest_exit_code": item.get("pytest_exit_code"),
                    "pytest_report_exit_code": item.get("pytest_report_exit_code"),
                    "tests_collected": item.get("tests_collected"),
                    "tests_total": item.get("tests_total"),
                }
                for (lane, version), item in sorted(lane_manifests.items())
            },
            "migration_evidence": [
                {
                    "path": item.get("_path"),
                    "manifest_passed": bool(item.get("passed", False)),
                    "counts_as_passed": validated_migration_manifest_passed(item),
                    "identity": item.get("identity"),
                    "environment_identity_ready": environment_identity_ready(item),
                    "install_evidence_ready": install_evidence_ready(item),
                    "backends": item.get("backends", []),
                    "passed_backends": item.get("passed_backends", []),
                    "expected_head_revision": item.get("expected_head_revision") or item.get("head_revision"),
                    "downgrade_target_revision": item.get("downgrade_target_revision"),
                }
                for item in migration_manifests
            ] + [
                {
                    "backend": backend,
                    "counts_as_passed": any(
                        validated_migration_backend_manifest_passed(item)
                        for item in items
                    ),
                    "manifests": [
                        {
                            "path": item.get("_path"),
                            "manifest_passed": bool(item.get("passed", False)),
                            "counts_as_passed": validated_migration_backend_manifest_passed(item),
                            "identity": item.get("identity"),
                            "backend": item.get("backend"),
                            "environment_identity_ready": environment_identity_ready(item),
                            "install_evidence_ready": install_evidence_ready(item),
                            "expected_head_revision": item.get("expected_head_revision"),
                            "downgrade_target_revision": item.get("downgrade_target_revision"),
                        }
                        for item in items
                    ],
                }
                for backend, items in sorted(migration_backend_manifests.items())
            ],
            "validated_manifests": [item.get("_path") for item in in_scope_manifests],
            "out_of_scope_validated_manifests": out_of_scope_manifests,
            "recognized_manifest_paths": [item.get("_path") for item in recognized_manifests],
            "ignored_json_paths": payload["ignored_json_paths"],
        },
    }
    report["warnings"] = [item for item in report["warnings"] if item]
    _write_report(repo_root / "docs" / "compliance", "validated_execution_report", report, "Validated Execution Report")
    return payload


def run_test_execution_gate(repo_root: Path) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    _ensure_repo_local_operator_state(repo_root)
    classification = verify_test_classification(repo_root, strict=True)
    validated = load_validated_execution_status(repo_root)
    failures: list[str] = []
    if not classification.get("passed", False):
        failures.append("Test classification manifest is invalid.")
    if not validated.get("in_scope_test_lanes_green", False):
        failures.append("Validated in-scope certification lane execution is incomplete.")
    if not validated.get("migration_portability_passed", False):
        failures.append("Migration portability validation across SQLite and PostgreSQL is missing.")
    payload = {
        "passed": not failures,
        "failures": failures,
        "warnings": [],
        "summary": {
            "classification_manifest_passed": bool(classification.get("passed", False)),
            "in_scope_test_lanes_green": bool(validated.get("in_scope_test_lanes_green", False)),
            "migration_portability_passed": bool(validated.get("migration_portability_passed", False)),
            "validated_test_lane_count": int(validated.get("test_lane_passed_count", 0)),
            "validated_test_lane_expected_count": int(validated.get("test_lane_expected_count", 0)),
        },
        "details": {
            "classification_failures": list(classification.get("failures", [])),
            "missing_test_lane_manifests": list(validated.get("test_lane_missing", [])),
        },
    }
    _write_report(repo_root / "docs" / "compliance", "test_execution_gate_report", payload, "Test Execution Gate Report")
    return payload
