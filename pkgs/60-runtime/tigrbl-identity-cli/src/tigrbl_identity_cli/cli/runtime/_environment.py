from __future__ import annotations

def build_validated_runner_profile_report(repo_root: Path, *, deployment: Any) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    support_manifest = _build_runner_support_manifest(repo_root)
    manifests_by_key = _validated_runtime_manifest_map(repo_root)
    all_expected_keys = [
        (profile, version)
        for profile, cfg in RUNTIME_VALIDATION_GROUPS.items()
        for version in cfg["supported_python_versions"]
    ]
    base_versions = list(RUNTIME_VALIDATION_GROUPS["base"]["supported_python_versions"])
    base_expected = [("base", version) for version in base_versions]
    base_manifests = [manifests_by_key[key] for key in base_expected if key in manifests_by_key]
    base_missing = [f"base@py{version}" for version in base_versions if ("base", version) not in manifests_by_key]
    base_failed = [
        f"base@py{version}"
        for version in base_versions
        if ("base", version) in manifests_by_key and not _runtime_manifest_counts_as_passed(manifests_by_key[("base", version)])
    ]
    application_probe_passed = bool(base_manifests) and not base_missing and not base_failed and all(bool(item.get("application_probe_passed", False)) for item in base_manifests)
    surface_probe_passed = bool(base_manifests) and not base_missing and not base_failed and all(runtime_surface_probe_ready(item) for item in base_manifests)
    surface_summary = _runtime_summary_from_manifests(base_manifests)
    application_message = (
        f"Validated runtime manifests confirm application-factory materialization for {len(base_manifests)}/{len(base_expected)} base environments."
        if application_probe_passed
        else (
            "Validated runtime manifests are missing or failing for the base application-factory environments: "
            + ", ".join(base_missing + base_failed)
            if (base_missing or base_failed)
            else "Validated runtime manifests do not yet prove base application-factory materialization."
        )
    )
    surface_message = (
        f"Validated runtime manifests confirm surface probes for {len(base_manifests)}/{len(base_expected)} base environments."
        if surface_probe_passed
        else (
            "Validated runtime manifests are missing or failing for the base surface-probe environments: "
            + ", ".join(base_missing + base_failed)
            if (base_missing or base_failed)
            else "Validated runtime manifests do not yet prove surface probes for the base environments."
        )
    )

    ready_count = 0
    missing_count = 0
    invalid_count = 0
    profiles: list[dict[str, Any]] = []
    application_hashes = {str(item.get("application_hash")) for item in manifests_by_key.values() if item.get("application_hash")}
    for adapter in iter_runner_adapters():
        support = dict((support_manifest.get("profiles") or {}).get(adapter.name, {}))
        matrix_profile = str(support.get("profile_name") or RUNNER_CERTIFICATION_MATRIX[adapter.name]["profile_name"])
        versions = list(RUNTIME_VALIDATION_GROUPS[matrix_profile]["supported_python_versions"])
        expected_keys = [(matrix_profile, version) for version in versions]
        expected_ids = _matrix_identities(matrix_profile, versions)
        present_ids = [f"{profile}@py{version}" for profile, version in expected_keys if (profile, version) in manifests_by_key]
        passed_ids = [
            f"{profile}@py{version}"
            for profile, version in expected_keys
            if _runtime_manifest_counts_as_passed(manifests_by_key.get((profile, version), {}))
        ]
        failed_ids = [
            f"{profile}@py{version}"
            for profile, version in expected_keys
            if (profile, version) in manifests_by_key and not _runtime_manifest_counts_as_passed(manifests_by_key[(profile, version)])
        ]
        missing_ids = [identity for identity in expected_ids if identity not in present_ids]
        present_manifests = [manifests_by_key[key] for key in expected_keys if key in manifests_by_key]
        installed = bool(present_manifests) and not missing_ids and all(bool(item.get("runner_available", False)) for item in present_manifests)
        serve_check_passed = bool(present_manifests) and not missing_ids and all(bool(item.get("serve_check_passed", False)) for item in present_manifests)
        if len(present_manifests) == 0:
            status = "missing"
            missing_count += 1
        elif not missing_ids and not failed_ids:
            status = "ready"
            ready_count += 1
        else:
            status = "invalid"
            invalid_count += 1
        diagnostics: list[dict[str, Any]] = []
        if missing_ids:
            diagnostics.append({
                "level": "warning",
                "code": "validated-manifest-missing",
                "message": "Validated runtime manifests are missing for one or more required matrix cells.",
                "identities": missing_ids,
            })
        if failed_ids:
            diagnostics.append({
                "level": "error",
                "code": "validated-execution-failed",
                "message": "One or more preserved runtime manifests did not satisfy the certification runtime criteria.",
                "identities": failed_ids,
                "reasons": {
                    f"{profile}@py{version}": _runtime_manifest_failure_reasons(manifests_by_key[(profile, version)])
                    for profile, version in expected_keys
                    if (profile, version) in manifests_by_key and not _runtime_manifest_counts_as_passed(manifests_by_key[(profile, version)])
                },
            })
        application_hash = None
        runtime_hash = None
        if present_manifests:
            app_hashes = {str(item.get("application_hash")) for item in present_manifests if item.get("application_hash")}
            run_hashes = {str(item.get("runtime_hash")) for item in present_manifests if item.get("runtime_hash")}
            if len(app_hashes) == 1:
                application_hash = next(iter(app_hashes))
            if len(run_hashes) == 1:
                runtime_hash = next(iter(run_hashes))
        serve_check_message = (
            f"Validated manifests confirm serve-check success for {len(passed_ids)}/{len(expected_ids)} required cells."
            if serve_check_passed
            else (
                "Validated runtime manifests are missing or failing serve-check evidence for required cells: "
                + ", ".join(missing_ids + failed_ids)
                if (missing_ids or failed_ids)
                else "Validated runtime manifests do not yet prove serve-check success for this runner."
            )
        )
        profiles.append(
            {
                "name": adapter.name,
                "display_name": adapter.display_name,
                "status": status,
                "installed": installed,
                "available_module": adapter.available_module_name(),
                "capabilities": [item.to_manifest() for item in adapter.capabilities],
                "flag_metadata": [item.to_manifest() for item in adapter.flag_metadata],
                "diagnostics": diagnostics,
                "application_hash": application_hash,
                "runtime_hash": runtime_hash,
                "serve_check": {
                    "executed": bool(present_manifests),
                    "passed": serve_check_passed,
                    "command": f"tigrbl-auth serve --check --server {adapter.name} --format json",
                    "message": serve_check_message,
                    "exit_code": 0 if serve_check_passed else None,
                },
                "validated_matrix": {
                    "matrix_profile": matrix_profile,
                    "expected_identities": expected_ids,
                    "present_identities": present_ids,
                    "passed_identities": passed_ids,
                    "missing_identities": missing_ids,
                    "failed_identities": failed_ids,
                    "identity_ready_count": sum(1 for item in present_manifests if environment_identity_ready(item)),
                    "install_evidence_ready_count": sum(1 for item in present_manifests if install_evidence_ready(item)),
                    "failure_reasons": {
                        f"{profile}@py{version}": _runtime_manifest_failure_reasons(manifests_by_key[(profile, version)])
                        for profile, version in expected_keys
                        if (profile, version) in manifests_by_key and not _runtime_manifest_counts_as_passed(manifests_by_key[(profile, version)])
                    },
                },
                **support,
            }
        )

    placeholder_supported_runner_names = [item["name"] for item in profiles if item.get("placeholder_supported")]
    declared_ci_installable_runner_names = [item["name"] for item in profiles if item.get("declared_installable_from_repository")]
    runtime_present_count = sum(1 for key in all_expected_keys if key in manifests_by_key)
    runtime_passed_count = sum(1 for key in all_expected_keys if _runtime_manifest_counts_as_passed(manifests_by_key.get(key, {})))
    validated_source = repo_root / "dist" / "validated-runs" / "collected-artifact-downloads.json"
    return {
        "generated_at": _utc_timestamp(),
        "deployment_profile": getattr(deployment, "profile", "baseline"),
        "report_mode": "validated-runs",
        "validated_artifact_source": validated_source.relative_to(repo_root).as_posix() if validated_source.exists() else None,
        "application_probe": {
            "passed": application_probe_passed,
            "app_factory": "unbound",
            "message": application_message,
            "error_type": None if application_probe_passed else "ValidatedRuntimeEvidenceMissing",
        },
        "surface_probe": {
            "executed": bool(base_manifests),
            "passed": surface_probe_passed,
            "message": surface_message,
            "endpoint_count": surface_summary["endpoint_count"],
            "passed_count": surface_summary["passed_count"],
            "failed_count": surface_summary["failed_count"],
            "probes": [],
        },
        "summary": {
            "runner_count": len(profiles),
            "ready_count": ready_count,
            "missing_count": missing_count,
            "invalid_count": invalid_count,
            "application_hash_invariant": len(application_hashes) == 1 if application_hashes else False,
            "pyproject_requires_python": support_manifest.get("requires_python"),
            "supported_python_versions": support_manifest.get("supported_python_versions", []),
            "placeholder_supported_runner_count": len(placeholder_supported_runner_names),
            "placeholder_supported_runner_names": placeholder_supported_runner_names,
            "declared_ci_installable_runner_count": len(declared_ci_installable_runner_names),
            "declared_ci_installable_runner_names": declared_ci_installable_runner_names,
            "declared_ci_install_probe_complete": len(declared_ci_installable_runner_names) == len(profiles),
            "execution_probes_enabled": True,
            "surface_probe_passed": surface_probe_passed,
            "surface_probe_endpoint_count": surface_summary["endpoint_count"],
            "surface_probe_passed_count": surface_summary["passed_count"],
            "surface_probe_failed_count": surface_summary["failed_count"],
            "serve_check_passed_count": sum(1 for item in profiles if item.get("serve_check", {}).get("passed")),
            "execution_probe_complete": runtime_present_count == len(all_expected_keys) and runtime_passed_count == len(all_expected_keys),
            "source_mode": "validated-runs",
            "required_runtime_cell_count": len(all_expected_keys),
            "validated_runtime_cell_count": runtime_present_count,
            "validated_runtime_cell_passed_count": runtime_passed_count,
            "validated_runtime_matrix_green": runtime_passed_count == len(all_expected_keys),
            "validated_runtime_identity_ready_count": sum(1 for item in manifests_by_key.values() if environment_identity_ready(item)),
            "validated_runtime_install_evidence_ready_count": sum(1 for item in manifests_by_key.values() if install_evidence_ready(item)),
            "validated_download_collection_present": validated_source.exists(),
        },
        "profiles": profiles,
    }


def run_runtime_foundation_check(
    repo_root: Path,
    *,
    strict: bool = True,
    report_dir: Path | None = None,
) -> int:
    repo_root = repo_root.resolve()
    report_dir = report_dir or (repo_root / "docs" / "compliance")
    report_dir.mkdir(parents=True, exist_ok=True)

    runtime_pkg = repo_root / "tigrbl_auth"
    tests_dir = repo_root / "tests"
    scripts_dir = repo_root / "scripts"
    pyproject_path = repo_root / "pyproject.toml"

    import_hits = {
        "runtime_package": _scan_patterns(
            runtime_pkg, FORBIDDEN_IMPORT_PATTERNS, rel_root=repo_root
        ),
        "tests": _scan_patterns(
            tests_dir, FORBIDDEN_IMPORT_PATTERNS, rel_root=repo_root
        ),
        "scripts": _scan_patterns(
            scripts_dir, FORBIDDEN_IMPORT_PATTERNS, rel_root=repo_root
        ),
    }
    runtime_private_hits = _scan_patterns(
        runtime_pkg, FORBIDDEN_RUNTIME_IMPORT_PATTERNS, rel_root=repo_root
    )

    fallback_hits: list[dict[str, str | int]] = []
    for rel in RUNTIME_FALLBACK_PATHS:
        path = repo_root / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for pattern in FORBIDDEN_FALLBACK_PATTERNS:
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                fallback_hits.append(
                    {
                        "path": str(path.relative_to(repo_root)),
                        "line": line,
                        "match": match.group(0).strip(),
                    }
                )

    dependency_hits = _scan_pyproject_forbidden_dependencies(pyproject_path)

    failures: list[str] = []
    if any(import_hits.values()):
        failures.append("FastAPI/Starlette imports remain in runtime, tests, or scripts.")
    if runtime_private_hits:
        failures.append(
            "Non-public Tigrbl imports remain in the active runtime package."
        )
    if dependency_hits:
        failures.append(
            "Forbidden FastAPI/Starlette dependencies remain in packaging metadata."
        )
    if fallback_hits:
        failures.append("Release-path framework fallbacks remain in active runtime files.")

    report: dict[str, Any] = {
        "scope": "tigrbl-runtime-foundation",
        "strict": strict,
        "passed": not failures,
        "summary": {
            "runtime_fastapi_starlette_hits": len(import_hits["runtime_package"]),
            "tests_fastapi_starlette_hits": len(import_hits["tests"]),
            "scripts_fastapi_starlette_hits": len(import_hits["scripts"]),
            "runtime_non_public_tigrbl_hits": len(runtime_private_hits),
            "pyproject_forbidden_dependency_hits": len(dependency_hits),
            "release_path_fallback_hits": len(fallback_hits),
        },
        "hits": {
            "fastapi_starlette": import_hits,
            "runtime_non_public_tigrbl": runtime_private_hits,
            "pyproject_forbidden_dependencies": dependency_hits,
            "release_path_fallbacks": fallback_hits,
        },
        "failures": failures,
    }

    json_path = report_dir / "tigrbl_runtime_foundation_report.json"
    md_path = report_dir / "tigrbl_runtime_foundation_report.md"
    nofs_json = report_dir / "no_fastapi_starlette_report.json"
    nofs_md = report_dir / "no_fastapi_starlette_report.md"
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Tigrbl Runtime Foundation Report",
        "",
        f"- Scope: `{report['scope']}`",
        f"- Strict: `{strict}`",
        f"- Passed: `{report['passed']}`",
        f"- Runtime FastAPI/Starlette hits: `{report['summary']['runtime_fastapi_starlette_hits']}`",
        f"- Test FastAPI/Starlette hits: `{report['summary']['tests_fastapi_starlette_hits']}`",
        f"- Script FastAPI/Starlette hits: `{report['summary']['scripts_fastapi_starlette_hits']}`",
        f"- Runtime non-public Tigrbl hits: `{report['summary']['runtime_non_public_tigrbl_hits']}`",
        f"- Pyproject forbidden dependency hits: `{report['summary']['pyproject_forbidden_dependency_hits']}`",
        f"- Release-path fallback hits: `{report['summary']['release_path_fallback_hits']}`",
        "",
    ]
    if failures:
        lines.extend(["## Failures", ""])
        lines.extend([f"- {item}" for item in failures])
        lines.append("")
    else:
        lines.extend(
            [
                "## Result",
                "",
                "The active runtime package is Tigrbl-only, release-path framework fallbacks were not detected, and no direct FastAPI/Starlette imports or metadata dependencies were found in runtime, tests, scripts, or packaging metadata.",
                "",
            ]
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")

    nofs_report = {
        "scope": "runtime package, tests, scripts, and packaging metadata",
        "root": {
            "runtime": str(runtime_pkg.relative_to(repo_root)),
            "tests": str(tests_dir.relative_to(repo_root)),
            "scripts": str(scripts_dir.relative_to(repo_root)),
            "metadata": str(pyproject_path.relative_to(repo_root)),
        },
        "direct_fastapi_starlette_imports_found": sum(
            len(v) for v in import_hits.values()
        ),
        "pyproject_forbidden_dependencies_found": dependency_hits,
        "hits": import_hits,
    }
    nofs_json.write_text(json.dumps(nofs_report, indent=2) + "\n", encoding="utf-8")
    nofs_lines = [
        "# No FastAPI / Starlette Import and Metadata Report",
        "",
        f"- Scope: `{nofs_report['scope']}`",
        f"- Runtime root: `{nofs_report['root']['runtime']}`",
        f"- Tests root: `{nofs_report['root']['tests']}`",
        f"- Scripts root: `{nofs_report['root']['scripts']}`",
        f"- Metadata file: `{nofs_report['root']['metadata']}`",
        f"- Direct import hits: `{nofs_report['direct_fastapi_starlette_imports_found']}`",
        f"- Forbidden metadata dependencies: `{len(dependency_hits)}`",
        "",
    ]
    if nofs_report["direct_fastapi_starlette_imports_found"] or dependency_hits:
        nofs_lines.extend(["## Findings", ""])
        for scope_name, scope_hits in import_hits.items():
            for hit in scope_hits:
                nofs_lines.append(
                    f"- `{scope_name}` → `{hit['path']}:{hit['line']}` — `{hit['match']}`"
                )
        for dep in dependency_hits:
            nofs_lines.append(
                f"- `pyproject.toml` declares forbidden dependency `{dep}`"
            )
        nofs_lines.append("")
    else:
        nofs_lines.extend(
            [
                "## Result",
                "",
                "No direct `fastapi` or `starlette` imports were found in the runtime package, tests, or scripts, and no forbidden `fastapi` or `starlette` dependencies were found in `pyproject.toml`.",
                "",
            ]
        )
    nofs_md.write_text("\n".join(nofs_lines), encoding="utf-8")

    return 1 if failures and strict else 0
