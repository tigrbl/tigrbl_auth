from __future__ import annotations

def build_install_substrate_report(
    repo_root: Path,
    *,
    profile: str | None = None,
    execute_import_probes: bool = True,
) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    current_profile = profile or "base"
    environment_identity = current_environment_identity(install_profile=current_profile, repo_root=repo_root)
    detected_pythons = _detect_supported_pythons()
    dependency_manifest = _pyproject_dependency_manifest(repo_root)
    constraint_consistency = _constraint_consistency(repo_root, dependency_manifest)
    dependency_lock_consistency = _dependency_lock_consistency(repo_root, dependency_manifest)
    tox_parser, tox_text = _read_tox(repo_root)
    tox_envlist = _extract_tox_envlist(tox_parser)
    tox_checks = _tox_section_checks(tox_text)
    tox_checks["envlist"] = tox_envlist
    workflow = _build_workflow_coverage(repo_root)

    static_failures: list[str] = []
    if dependency_manifest["workspace_sources_present"]:
        static_failures.append("pyproject.toml still declares forbidden workspace dependency sources")
    if dependency_manifest["forbidden_dependency_references"]:
        static_failures.append("One or more dependency declarations still use forbidden local/editable sources")
    static_failures.extend(constraint_consistency["mismatches"])
    static_failures.extend(dependency_lock_consistency["failures"])
    if len(tox_envlist) != len(CERTIFICATION_TOX_ENVS):
        static_failures.append("tox envlist does not match the retained certification tox matrix")
    if set(tox_envlist) != set(CERTIFICATION_TOX_ENVS):
        static_failures.append("tox envlist membership drifts from the retained certification tox matrix")
    if not tox_checks["passed"]:
        static_failures.append("tox install-substrate commands are incomplete")
    if not workflow["install_profiles_workflow_passed"]:
        static_failures.append("ci-install-profiles workflow does not cover the full retained runtime matrix")
    if not workflow["release_gates_workflow_passed"]:
        static_failures.append("ci-release-gates workflow does not cover the retained certification lanes and promotion jobs")

    expected_modules = _expected_modules_for_profile(current_profile)
    module_results = _probe_modules(expected_modules) if execute_import_probes else []
    runtime_surface_results = _runtime_surface_probe(repo_root) if execute_import_probes else []
    import_failures = [item for item in module_results if not item.get("passed")]
    runtime_surface_failures = [item for item in runtime_surface_results if not item.get("passed")]

    warnings: list[str] = []
    if not _current_python_supported():
        warnings.append("Current container Python is outside the declared certification support range (>=3.10,<3.13).")
    unavailable_supported = [item["version"] for item in detected_pythons if not item["available"]]
    if unavailable_supported:
        warnings.append(
            f"The current container does not provide supported interpreter binaries for: {', '.join(unavailable_supported)}."
        )
    dependency_python_blockers = dependency_lock_consistency.get("python_support_blockers", [])
    if dependency_python_blockers:
        warnings.extend(str(item) for item in dependency_python_blockers)

    failures = list(static_failures)
    if not _current_python_supported():
        failures.append("The current environment is outside the declared certification interpreter support range.")
    if unavailable_supported:
        failures.append("The current environment does not provide the full supported interpreter matrix required for clean-room certification.")
    if execute_import_probes and import_failures:
        failures.append("The current environment is missing one or more modules required by the selected install profile.")
    if execute_import_probes and runtime_surface_failures:
        failures.append("One or more runtime import surfaces could not be resolved from the source tree.")

    summary = {
        "static_manifest_passed": not static_failures,
        "passed": not failures,
        "profile": current_profile,
        "current_profile_identity": runtime_identity(current_profile),
        "environment_identity_present": True,
        "current_python": sys.version.split()[0],
        "current_python_supported": _current_python_supported(),
        "expected_supported_python_versions": list(SUPPORTED_PYTHON_VERSIONS),
        "expected_supported_python_count": len(SUPPORTED_PYTHON_VERSIONS),
        "detected_supported_python_count": sum(1 for item in detected_pythons if item["available"]),
        "declared_runtime_matrix_env_count": len(RUNTIME_MATRIX_ENVS),
        "declared_test_lane_env_count": len(TEST_LANE_ENVS),
        "declared_certification_tox_env_count": len(CERTIFICATION_TOX_ENVS),
        "tox_env_count": len(tox_envlist),
        "tox_envs_with_pip_check_count": tox_checks["pip_check_ok_count"],
        "tox_envs_with_install_probe_count": tox_checks["install_probe_ok_count"],
        "tox_section_template_count": tox_checks["section_count"],
        "tox_envs_declare_pip_check": tox_checks["pip_check_ok_count"] == tox_checks["section_count"],
        "tox_envs_declare_install_probe": tox_checks["install_probe_ok_count"] == tox_checks["section_count"],
        "workspace_sources_present": dependency_manifest["workspace_sources_present"],
        "workspace_sources_declared": dependency_manifest["workspace_sources_declared"],
        "first_party_workspace_source_count": dependency_manifest["first_party_workspace_source_count"],
        "forbidden_workspace_source_count": dependency_manifest["forbidden_workspace_source_count"],
        "forbidden_dependency_reference_count": len(dependency_manifest["forbidden_dependency_references"]),
        "base_dependency_count": dependency_manifest["dependency_count"],
        "base_exact_pinned_dependency_count": dependency_manifest["exact_pinned_dependency_count"],
        "dependency_lock_manifest_present": (repo_root / "constraints" / "dependency-lock.json").exists(),
        "dependency_lock_install_profile_count": dependency_lock_consistency["install_profile_count"],
        "install_profiles_workflow_present": workflow["install_profiles_workflow_present"],
        "release_gates_workflow_present": workflow["release_gates_workflow_present"],
        "install_profiles_runtime_env_present_count": workflow["install_profiles_runtime_env_present_count"],
        "release_gates_runtime_env_present_count": workflow["release_gates_runtime_env_present_count"],
        "release_gates_test_lane_env_present_count": workflow["release_gates_test_lane_env_present_count"],
        "release_gates_extra_env_present_count": workflow["release_gates_extra_env_present_count"],
        "install_profiles_artifact_upload_present": workflow["install_profiles_artifact_upload_present"],
        "release_gates_artifact_upload_present": workflow["release_gates_artifact_upload_present"],
        "current_profile_expected_module_count": len(expected_modules),
        "current_profile_import_probe_passed_count": sum(1 for item in module_results if item.get("passed")),
        "current_profile_import_probe_failed_count": sum(1 for item in module_results if not item.get("passed")),
        "current_profile_import_probe_passed": not import_failures,
        "runtime_surface_probe_count": len(runtime_surface_results),
        "runtime_surface_probe_failed_count": len(runtime_surface_failures),
        "runtime_surface_probe_passed": not runtime_surface_failures,
    }

    profiles = {
        name: {
            "constraints": list(details["constraints"]),
            "extras": list(details["extras"]),
            "expected_modules": [item["module"] for item in _expected_modules_for_profile(name)],
        }
        for name, details in PROFILE_TOGGLES.items()
    }

    return {
        "generated_at": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "passed": not failures,
        "summary": summary,
        "failures": failures,
        "warnings": warnings,
        "detected_supported_pythons": detected_pythons,
        "dependency_manifest": dependency_manifest,
        "constraints_consistency": constraint_consistency,
        "dependency_lock_consistency": dependency_lock_consistency,
        "tox": tox_checks,
        "workflow": workflow,
        "profiles": profiles,
        "identity": runtime_identity(current_profile),
        "environment_identity": environment_identity,
        "current_environment_probe": {
            "profile": current_profile,
            "identity": runtime_identity(current_profile),
            "environment_identity": environment_identity,
            "python": sys.version.split()[0],
            "python_supported": _current_python_supported(),
            "module_results": module_results,
            "runtime_surface_results": runtime_surface_results,
        },
    }


def write_install_substrate_report(
    repo_root: Path,
    *,
    profile: str | None = None,
    report_dir: Path | None = None,
    artifact_dir: Path | None = None,
    execute_import_probes: bool = True,
) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    report_dir = report_dir or (repo_root / "docs" / "compliance")
    report_dir.mkdir(parents=True, exist_ok=True)
    payload = build_install_substrate_report(repo_root, profile=profile, execute_import_probes=execute_import_probes)
    payload = sanitize_local_paths(payload, repo_root)
    json_path = report_dir / "install_substrate_report.json"
    md_path = report_dir / "install_substrate_report.md"
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Install Substrate Report",
        "",
        f"- Generated at: `{payload.get('generated_at')}`",
        f"- Passed: `{payload.get('passed')}`",
        f"- Static manifest passed: `{payload['summary']['static_manifest_passed']}`",
        f"- Profile: `{payload['summary']['profile']}`",
        f"- Profile identity: `{payload['summary']['current_profile_identity']}`",
        f"- Environment identity present: `{payload['summary']['environment_identity_present']}`",
        f"- Current Python: `{payload['summary']['current_python']}`",
        f"- Current Python supported: `{payload['summary']['current_python_supported']}`",
        f"- Expected supported Python versions: `{', '.join(payload['summary']['expected_supported_python_versions'])}`",
        f"- Detected supported Python binaries: `{payload['summary']['detected_supported_python_count']}` / `{payload['summary']['expected_supported_python_count']}`",
        f"- Certification tox envs declared: `{payload['summary']['declared_certification_tox_env_count']}`",
        f"- Runtime matrix envs declared: `{payload['summary']['declared_runtime_matrix_env_count']}`",
        f"- Test lane envs declared: `{payload['summary']['declared_test_lane_env_count']}`",
        f"- Tox templates with pip check: `{payload['summary']['tox_envs_with_pip_check_count']}` / `{payload['summary']['tox_section_template_count']}`",
        f"- Tox templates with install probe: `{payload['summary']['tox_envs_with_install_probe_count']}` / `{payload['summary']['tox_section_template_count']}`",
        f"- Current profile import probe passed: `{payload['summary']['current_profile_import_probe_passed']}`",
        f"- Runtime surface probe passed: `{payload['summary']['runtime_surface_probe_passed']}`",
        "",
    ]
    if payload.get("failures"):
        lines.extend(["## Failures", ""])
        lines.extend([f"- {item}" for item in payload["failures"]])
        lines.append("")
    if payload.get("warnings"):
        lines.extend(["## Warnings", ""])
        lines.extend([f"- {item}" for item in payload["warnings"]])
        lines.append("")
    lines.extend(["## Current environment import probe", ""])
    for item in payload.get("current_environment_probe", {}).get("module_results", []):
        lines.append(f"- `{item['module']}` ({item['package']}) → passed=`{item['passed']}` message=`{item['message']}`")
    lines.append("")
    lines.extend(["## Runtime import surfaces", ""])
    for item in payload.get("current_environment_probe", {}).get("runtime_surface_results", []):
        lines.append(f"- `{item['module']}` → passed=`{item['passed']}` message=`{item['message']}`")
    lines.append("")
    lines.extend(["## Detected supported interpreters", ""])
    for item in payload.get("detected_supported_pythons", []):
        lines.append(f"- `{item['version']}` → available=`{item['available']}` path=`{item['path']}`")
    lines.append("")
    workflow = payload.get("workflow", {})
    lines.extend(
        [
            "## Workflow coverage",
            "",
            f"- install_profiles_workflow_present: `{workflow.get('install_profiles_workflow_present')}`",
            f"- release_gates_workflow_present: `{workflow.get('release_gates_workflow_present')}`",
            f"- install_profiles_runtime_env_present_count: `{workflow.get('install_profiles_runtime_env_present_count')}`",
            f"- release_gates_runtime_env_present_count: `{workflow.get('release_gates_runtime_env_present_count')}`",
            f"- release_gates_test_lane_env_present_count: `{workflow.get('release_gates_test_lane_env_present_count')}`",
            f"- release_gates_extra_env_present_count: `{workflow.get('release_gates_extra_env_present_count')}`",
            f"- install_profiles_artifact_upload_present: `{workflow.get('install_profiles_artifact_upload_present')}`",
            f"- release_gates_artifact_upload_present: `{workflow.get('release_gates_artifact_upload_present')}`",
            "",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")

    if artifact_dir is not None:
        artifact_dir = artifact_dir.resolve()
        artifact_dir.mkdir(parents=True, exist_ok=True)
        profile_name = payload["summary"]["profile"]
        py_tag = f"py{sys.version_info.major}{sys.version_info.minor}"
        tox_env = str(payload.get("environment_identity", {}).get("tox_env") or "").strip()
        artifacts = [artifact_dir / f"{profile_name}.json", artifact_dir / f"{profile_name}-{py_tag}.json"]
        if tox_env:
            artifacts.append(artifact_dir / f"{tox_env}.json")
        for artifact in artifacts:
            artifact.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


__all__ = [
    "CERTIFICATION_TOX_ENVS",
    "PROFILE_TOGGLES",
    "RUNTIME_MATRIX_ENVS",
    "TEST_LANE_ENVS",
    "SUPPORTED_PYTHON_VERSIONS",
    "build_install_substrate_report",
    "write_install_substrate_report",
]
