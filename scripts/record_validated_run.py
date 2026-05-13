from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tigrbl_auth.cli.certification_evidence import (
    current_environment_identity,
    lane_identity,
    migration_identity,
    runtime_identity,
    validated_migration_backend_manifest_passed,
    validated_migration_manifest_passed,
    validated_runtime_manifest_passed,
    validated_test_lane_manifest_passed,
)


def _read_json(path: Path | None) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path is not None and path.exists() else {}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _sha256_file(path: Path | None) -> str | None:
    if path is None or not path.exists() or not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _current_version() -> str:
    pyproject = ROOT / "pyproject.toml"
    if not pyproject.exists():
        return "0.0.0"
    for line in pyproject.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("version") and "=" in line:
            return line.split("=", 1)[1].strip().strip('"')
    return "0.0.0"


def _write_report(stem: str, title: str, payload: dict[str, Any]) -> None:
    report_dir = ROOT / "docs" / "compliance"
    report_dir.mkdir(parents=True, exist_ok=True)
    _write_json(report_dir / f"{stem}.json", payload)
    lines = [f"# {title}", "", f"- Passed: `{payload.get('passed', False)}`", ""]
    if payload.get("summary"):
        lines.extend(["## Summary", ""])
        for key, value in payload["summary"].items():
            lines.append(f"- {key}: `{value}`")
        lines.append("")
    if payload.get("failures"):
        lines.extend(["## Failures", ""])
        lines.extend([f"- {item}" for item in payload["failures"]])
        lines.append("")
    if payload.get("warnings"):
        lines.extend(["## Warnings", ""])
        lines.extend([f"- {item}" for item in payload["warnings"]])
        lines.append("")
    if payload.get("details"):
        lines.extend(["## Details", ""])
        details = payload["details"]
        if isinstance(details, dict):
            for key, value in details.items():
                lines.append(f"- {key}: `{value}`")
        else:
            lines.extend([f"- {item}" for item in details])
        lines.append("")
    (report_dir / f"{stem}.md").write_text("\n".join(lines), encoding="utf-8")


def _coerce_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _pytest_summary(report: dict[str, Any]) -> dict[str, int]:
    summary = report.get("summary", {}) if isinstance(report, dict) else {}

    def _count(key: str) -> int:
        value = summary.get(key, 0)
        try:
            return int(value)
        except (TypeError, ValueError):
            return 0

    collected = _count("collected")
    total = _count("total")
    return {
        "tests_collected": max(collected, total),
        "tests_total": total,
        "tests_passed": _count("passed"),
        "tests_failed": _count("failed"),
        "tests_error": max(_count("error"), _count("errors")),
        "tests_skipped": _count("skipped"),
        "tests_xfailed": _count("xfailed"),
        "tests_xpassed": _count("xpassed"),
    }


def _out_root() -> Path:
    path = Path(os.environ.get("TIGRBL_AUTH_VALIDATED_RUN_ROOT", str(ROOT / "dist" / "validated-runs")))
    path.mkdir(parents=True, exist_ok=True)
    return path


def _write_manifest(stem: str, payload: dict[str, Any]) -> int:
    out_path = _out_root() / f"{stem}.json"
    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0


def _base_payload(kind: str) -> dict[str, Any]:
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    return {
        "schema_version": 4,
        "kind": kind,
        "generated_at": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "python_version": python_version,
        "tox_env": os.environ.get("TOX_ENV_NAME"),
        "matrix_profile": os.environ.get("TIGRBL_AUTH_MATRIX_PROFILE"),
        "repository_version": _current_version(),
        "validated_run_root": _relative(_out_root()),
    }


def _py_tag() -> str:
    return f"py{sys.version_info.major}{sys.version_info.minor}"


def _relative(path: Path | None) -> str | None:
    if path is None:
        return None
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def _first_existing(candidates: list[Path]) -> Path | None:
    seen: set[Path] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        if candidate.exists():
            return candidate
    return None


def _runtime_smoke_candidates(matrix_profile: str | None, runner: str | None) -> list[Path]:
    runtime_smoke_root = ROOT / "dist" / "runtime-smoke"
    runner_label = runner or "base"
    py_tag = _py_tag()
    candidates: list[Path] = []
    tox_env = os.environ.get("TOX_ENV_NAME", "").strip()
    if tox_env:
        candidates.append(runtime_smoke_root / f"{tox_env}.json")
    if matrix_profile:
        candidates.extend(
            [
                runtime_smoke_root / f"{matrix_profile}-{runner_label}.json",
                runtime_smoke_root / f"{matrix_profile}-{py_tag}-{runner_label}.json",
                runtime_smoke_root / f"{py_tag}-{matrix_profile}-{runner_label}.json",
            ]
        )
    return candidates


def _serve_check_candidates(matrix_profile: str | None, runner: str | None) -> list[Path]:
    runtime_smoke_root = ROOT / "dist" / "runtime-smoke"
    candidates: list[Path] = []
    tox_env = os.environ.get("TOX_ENV_NAME", "").strip()
    if tox_env:
        candidates.append(runtime_smoke_root / tox_env / "serve-check.json")
        candidates.append(runtime_smoke_root / f"serve-check-{tox_env}.json")
    if matrix_profile == "sqlite-uvicorn":
        candidates.append(runtime_smoke_root / "sqlite-uvicorn-serve-check.json")
    elif matrix_profile == "postgres-hypercorn":
        candidates.append(runtime_smoke_root / "postgres-hypercorn-serve-check.json")
    elif matrix_profile == "tigrcorn":
        candidates.append(runtime_smoke_root / "tigrcorn-serve-check.json")
    elif matrix_profile == "devtest":
        candidates.append(runtime_smoke_root / "devtest-uvicorn-serve-check.json")
    elif matrix_profile == "release-gates":
        if runner:
            candidates.append(runtime_smoke_root / f"release-gates-{runner}-serve-check.json")
    elif runner:
        candidates.append(runtime_smoke_root / f"{matrix_profile or runner}-{runner}-serve-check.json")
    return candidates


def _default_install_profile(*, matrix_profile: str | None = None, lane: str | None = None) -> str:
    explicit = str(os.environ.get("TIGRBL_AUTH_INSTALL_PROFILE") or "").strip()
    if explicit:
        return explicit
    if lane:
        return f"test-{lane}"
    if matrix_profile:
        return matrix_profile
    return "base"


def _install_substrate_candidates(install_profile: str | None) -> list[Path]:
    install_root = ROOT / "dist" / "install-substrate"
    report_root = ROOT / "docs" / "compliance"
    tox_env = os.environ.get("TOX_ENV_NAME", "").strip()
    py_tag = _py_tag()
    candidates: list[Path] = []
    if tox_env:
        candidates.append(install_root / f"{tox_env}.json")
    if install_profile:
        candidates.append(install_root / f"{install_profile}-{py_tag}.json")
        candidates.append(install_root / f"{install_profile}.json")
    candidates.append(report_root / "install_substrate_report.json")
    return candidates


def _install_substrate_details(install_profile: str) -> tuple[Path | None, dict[str, Any], dict[str, Any], dict[str, Any]]:
    install_path = _first_existing(_install_substrate_candidates(install_profile))
    install_payload = _read_json(install_path)
    summary = install_payload.get("summary", {}) if isinstance(install_payload, dict) else {}
    env_identity = install_payload.get("environment_identity") if isinstance(install_payload.get("environment_identity"), dict) else {}
    if not env_identity:
        probe = install_payload.get("current_environment_probe")
        if isinstance(probe, dict) and isinstance(probe.get("environment_identity"), dict):
            env_identity = probe.get("environment_identity")
    return install_path, install_payload, summary, env_identity if isinstance(env_identity, dict) else {}


def _environment_identity(*, matrix_profile: str | None = None, install_profile: str | None = None, lane: str | None = None, runner: str | None = None, preferred: dict[str, Any] | None = None, fallback: dict[str, Any] | None = None) -> dict[str, Any]:
    for candidate in (preferred, fallback):
        if isinstance(candidate, dict) and candidate:
            return dict(candidate)
    return current_environment_identity(matrix_profile=matrix_profile, install_profile=install_profile, test_lane=lane, runner=runner, repo_root=ROOT)


def _cmd_runtime_profile(args: argparse.Namespace) -> int:
    payload = _base_payload("runtime-profile")
    runtime_report_path = ROOT / "docs" / "compliance" / "runtime_profile_report.json"
    runtime_report = _read_json(runtime_report_path)
    runner = args.runner or os.environ.get("TIGRBL_AUTH_RUNNER") or None
    matrix_profile = str(payload.get("matrix_profile") or "unknown")
    install_profile = _default_install_profile(matrix_profile=matrix_profile)

    smoke_path = _first_existing(_runtime_smoke_candidates(matrix_profile, runner))
    smoke = _read_json(smoke_path)
    serve_check_path = _first_existing(_serve_check_candidates(matrix_profile, runner)) if runner else None
    serve_check = _read_json(serve_check_path)
    install_path, install_payload, install_summary, install_env_identity = _install_substrate_details(install_profile)

    smoke_passed = bool(smoke.get("passed", False))
    application_probe_passed = bool(smoke.get("application_probe_passed", False) or runtime_report.get("application_probe", {}).get("passed", False))
    surface_probe_payload = smoke.get("surface_probe", {}) if isinstance(smoke.get("surface_probe"), dict) else {}
    surface_probe_passed = bool(smoke.get("surface_probe_passed", False) or surface_probe_payload.get("passed", False))
    runner_available = bool(smoke.get("runner_available", False)) if runner else None
    serve_check_passed = bool(serve_check.get("launch_ready", False) and serve_check.get("server") == runner) if runner else None
    if runner and not serve_check_passed:
        serve_check_passed = bool(serve_check.get("selected_runner_profile", {}).get("status") == "ready") and bool(serve_check.get("application_probe", {}).get("passed", False))

    smoke_env_identity = smoke.get("environment_identity") if isinstance(smoke.get("environment_identity"), dict) else {}
    environment_identity = _environment_identity(matrix_profile=matrix_profile, install_profile=install_profile, runner=runner, preferred=smoke_env_identity, fallback=install_env_identity)

    payload.update(
        {
            "identity": runtime_identity(matrix_profile, payload["python_version"]),
            "environment_identity": environment_identity,
            "runner": runner,
            "install_profile": install_profile,
            "install_substrate_artifact": _relative(install_path),
            "install_substrate_artifact_sha256": _sha256_file(install_path),
            "install_substrate_identity": install_payload.get("identity"),
            "install_substrate_environment_identity": install_env_identity,
            "install_substrate_passed": bool(install_payload.get("passed", False)),
            "install_substrate_static_manifest_passed": bool(install_summary.get("static_manifest_passed", False)),
            "install_substrate_current_profile_import_probe_passed": bool(install_summary.get("current_profile_import_probe_passed", False)),
            "install_substrate_runtime_surface_probe_passed": bool(install_summary.get("runtime_surface_probe_passed", False)),
            "runtime_profile_report_artifact": _relative(runtime_report_path),
            "runtime_profile_report_sha256": _sha256_file(runtime_report_path),
            "runtime_profile_summary": runtime_report.get("summary", {}),
            "runtime_report_mode": runtime_report.get("report_mode") or runtime_report.get("summary", {}).get("source_mode"),
            "runtime_smoke_artifact": _relative(smoke_path),
            "runtime_smoke_artifact_sha256": _sha256_file(smoke_path),
            "runtime_smoke_environment_identity": smoke_env_identity,
            "runtime_smoke_passed": smoke_passed,
            "application_probe_passed": application_probe_passed,
            "surface_probe_passed": surface_probe_passed,
            "surface_probe_endpoint_count": _coerce_int(smoke.get("surface_probe_endpoint_count")) or _coerce_int(surface_probe_payload.get("endpoint_count")),
            "surface_probe_passed_count": _coerce_int(smoke.get("surface_probe_passed_count")) or _coerce_int(surface_probe_payload.get("passed_count")),
            "surface_probe_failed_count": _coerce_int(smoke.get("surface_probe_failed_count")) or _coerce_int(surface_probe_payload.get("failed_count")),
            "application_hash": smoke.get("application_hash"),
            "runtime_hash": smoke.get("runtime_hash"),
            "runner_available": runner_available,
            "serve_check_artifact": _relative(serve_check_path),
            "serve_check_artifact_sha256": _sha256_file(serve_check_path),
            "serve_check_passed": serve_check_passed,
            "serve_check_exit_code": serve_check.get("selected_runner_profile", {}).get("serve_check", {}).get("exit_code") if isinstance(serve_check, dict) else None,
        }
    )
    payload["passed"] = validated_runtime_manifest_passed(payload)
    stem = f"runtime-{matrix_profile}-py{payload['python_version'].replace('.', '')}"
    return _write_manifest(stem, payload)


def _cmd_test_lane(args: argparse.Namespace) -> int:
    payload = _base_payload("test-lane")
    lane = args.lane or os.environ.get("TIGRBL_AUTH_TEST_LANE") or "unknown"
    install_profile = _default_install_profile(lane=lane)
    report_path = Path(args.report).resolve() if args.report else None
    report = _read_json(report_path)
    install_path, install_payload, install_summary, install_env_identity = _install_substrate_details(install_profile)

    pytest_exit_code = _coerce_int(args.pytest_exit_code)
    pytest_report_exit_code = _coerce_int(report.get("exitcode"))
    summary = _pytest_summary(report)
    report_present = bool(report_path is not None and report_path.exists() and report)
    environment_identity = _environment_identity(install_profile=install_profile, lane=lane, preferred=install_env_identity)

    payload.update(
        {
            "identity": lane_identity(lane, payload["python_version"]),
            "environment_identity": environment_identity,
            "lane": lane,
            "install_profile": install_profile,
            "install_substrate_artifact": _relative(install_path),
            "install_substrate_artifact_sha256": _sha256_file(install_path),
            "install_substrate_identity": install_payload.get("identity"),
            "install_substrate_environment_identity": install_env_identity,
            "install_substrate_passed": bool(install_payload.get("passed", False)),
            "install_substrate_static_manifest_passed": bool(install_summary.get("static_manifest_passed", False)),
            "install_substrate_current_profile_import_probe_passed": bool(install_summary.get("current_profile_import_probe_passed", False)),
            "install_substrate_runtime_surface_probe_passed": bool(install_summary.get("runtime_surface_probe_passed", False)),
            "pytest_report_artifact": _relative(report_path),
            "pytest_report_sha256": _sha256_file(report_path),
            "pytest_report_present": report_present,
            "pytest_exit_code": pytest_exit_code,
            "pytest_report_exit_code": pytest_report_exit_code,
            **summary,
        }
    )
    payload["passed"] = validated_test_lane_manifest_passed(payload)
    stem = f"test-{lane}-py{payload['python_version'].replace('.', '')}"
    return _write_manifest(stem, payload)


def _cmd_migration_portability(args: argparse.Namespace) -> int:
    payload = _base_payload("migration-portability")
    install_profile = _default_install_profile(matrix_profile="migration-portability")
    report_path = Path(args.report).resolve() if args.report else None
    report = _read_json(report_path)
    install_path, install_payload, install_summary, install_env_identity = _install_substrate_details(install_profile)
    environment_identity = _environment_identity(install_profile=install_profile, preferred=install_env_identity)

    pytest_report_path = ROOT / str(report.get("pytest_report_artifact")) if report.get("pytest_report_artifact") else None
    backend_manifests: list[dict[str, Any]] = []
    for backend in ("sqlite", "postgres"):
        backend_result = report.get("backend_results", {}).get(backend, {})
        artifact_map = backend_result.get("artifacts", {}) if isinstance(backend_result, dict) else {}
        backend_payload = {
            "schema_version": 5,
            "kind": "migration-portability-backend",
            "generated_at": payload["generated_at"],
            "python_version": payload["python_version"],
            "tox_env": payload.get("tox_env"),
            "matrix_profile": payload.get("matrix_profile"),
            "repository_version": payload.get("repository_version"),
            "validated_run_root": payload.get("validated_run_root"),
            "identity": migration_identity(f"migration-portability-{backend}", payload["python_version"]),
            "environment_identity": environment_identity,
            "install_profile": install_profile,
            "install_substrate_artifact": _relative(install_path),
            "install_substrate_artifact_sha256": _sha256_file(install_path),
            "install_substrate_identity": install_payload.get("identity"),
            "install_substrate_environment_identity": install_env_identity,
            "install_substrate_passed": bool(install_payload.get("passed", False)),
            "install_substrate_static_manifest_passed": bool(install_summary.get("static_manifest_passed", False)),
            "install_substrate_current_profile_import_probe_passed": bool(install_summary.get("current_profile_import_probe_passed", False)),
            "install_substrate_runtime_surface_probe_passed": bool(install_summary.get("runtime_surface_probe_passed", False)),
            "backend": backend,
            "available": bool(backend_result.get("available", False)),
            "passed": bool(backend_result.get("passed", False)),
            "upgrade_passed": bool(backend_result.get("upgrade_passed", False)),
            "downgrade_passed": bool(backend_result.get("downgrade_passed", False)),
            "reapply_passed": bool(backend_result.get("reapply_passed", False)),
            "artifacts": artifact_map,
            "artifact_sha256": {name: _sha256_file(ROOT / str(path)) for name, path in artifact_map.items()},
            "expected_head_revision": backend_result.get("expected_head_revision") or report.get("expected_head_revision"),
            "downgrade_target_revision": backend_result.get("downgrade_target_revision") or report.get("downgrade_target_revision"),
            "downgraded_revision": backend_result.get("downgraded_revision"),
            "head_revision_after_upgrade": backend_result.get("head_revision_after_upgrade"),
            "head_revision_after_downgrade": backend_result.get("head_revision_after_downgrade"),
            "head_revision_after_reapply": backend_result.get("head_revision_after_reapply"),
            "pytest_report_artifact": report.get("pytest_report_artifact"),
            "pytest_report_sha256": _sha256_file(pytest_report_path),
            "pytest_exit_code": _coerce_int(report.get("pytest_exit_code")),
        }
        backend_payload["passed"] = validated_migration_backend_manifest_passed(backend_payload)
        backend_stem = f"migration-portability-{backend}-py{payload['python_version'].replace('.', '')}"
        _write_manifest(backend_stem, backend_payload)
        backend_manifests.append(
            {
                "backend": backend,
                "path": _relative(_out_root() / f"{backend_stem}.json"),
                "sha256": _sha256_file(_out_root() / f"{backend_stem}.json"),
                "passed": backend_payload["passed"],
            }
        )
    payload.update(
        {
            "identity": migration_identity("migration-portability", payload["python_version"]),
            "environment_identity": environment_identity,
            "install_profile": install_profile,
            "install_substrate_artifact": _relative(install_path),
            "install_substrate_artifact_sha256": _sha256_file(install_path),
            "install_substrate_identity": install_payload.get("identity"),
            "install_substrate_environment_identity": install_env_identity,
            "install_substrate_passed": bool(install_payload.get("passed", False)),
            "install_substrate_static_manifest_passed": bool(install_summary.get("static_manifest_passed", False)),
            "install_substrate_current_profile_import_probe_passed": bool(install_summary.get("current_profile_import_probe_passed", False)),
            "install_substrate_runtime_surface_probe_passed": bool(install_summary.get("runtime_surface_probe_passed", False)),
            "report_artifact": _relative(report_path),
            "report_sha256": _sha256_file(report_path),
            "backends": list(report.get("validated_backends", [])),
            "required_backends": list(report.get("required_backends", [])),
            "passed_backends": list(report.get("passed_backends", [])),
            "backend_results": report.get("backend_results", {}),
            "pytest_report_artifact": report.get("pytest_report_artifact"),
            "pytest_report_sha256": _sha256_file(pytest_report_path),
            "pytest_exit_code": _coerce_int(report.get("pytest_exit_code")),
            "pytest_summary": report.get("pytest_summary", {}),
            "revision_inventory": report.get("revision_inventory", []),
            "expected_head_revision": report.get("expected_head_revision"),
            "head_revision": report.get("head_revision"),
            "downgrade_target_revision": report.get("downgrade_target_revision"),
            "backend_manifests": backend_manifests,
            "report_passed": bool(report.get("passed", False)),
        }
    )
    payload["passed"] = validated_migration_manifest_passed(payload)
    return _write_manifest(f"migration-portability-py{payload['python_version'].replace('.', '')}", payload)


def _cmd_tier3_evidence(args: argparse.Namespace) -> int:
    payload = _base_payload("tier3-evidence")
    current_path = ROOT / "docs" / "compliance" / "current_state_report.json"
    validated_path = ROOT / "docs" / "compliance" / "validated_execution_report.json"
    runtime_path = ROOT / "docs" / "compliance" / "runtime_profile_report.json"
    release_gate_path = ROOT / "docs" / "compliance" / "release_gate_report.json"
    final_gate_path = ROOT / "docs" / "compliance" / "final_release_gate_report.json"
    collected_path = ROOT / "dist" / "validated-runs" / "collected-artifact-downloads.json"

    current = _read_json(current_path)
    validated = _read_json(validated_path)
    runtime = _read_json(runtime_path)
    release_gate = _read_json(release_gate_path)
    final_gate = _read_json(final_gate_path)
    recognized_manifest_paths = list((validated.get("details") or {}).get("recognized_manifest_paths", []))
    validated_manifest_paths = list((validated.get("details") or {}).get("validated_manifests", []))
    out_of_scope_manifest_paths = [
        str(item.get("path"))
        for item in ((validated.get("details") or {}).get("out_of_scope_validated_manifests", []) or [])
        if item.get("path")
    ]
    required_runtime_count = int((validated.get("summary") or {}).get("runtime_matrix_expected_count", 0))
    required_test_lane_count = int((validated.get("summary") or {}).get("test_lane_expected_count", 0))
    required_inventory_count = required_runtime_count + required_test_lane_count + 2
    runtime_report_generated_from_validated_runs = bool(
        runtime.get("report_mode") == "validated-runs"
        or (runtime.get("summary") or {}).get("source_mode") == "validated-runs"
    )
    validated_inventory_present_count = int((validated.get("summary") or {}).get("validated_inventory_present_count", 0))
    minimum_inventory_complete = bool((validated.get("summary") or {}).get("validated_inventory_complete", False))
    failures: list[str] = []
    if not validated:
        failures.append("Validated execution report is missing.")
    if not runtime:
        failures.append("Runtime profile report is missing.")
    if not release_gate:
        failures.append("Release gate report is missing.")
    if not final_gate:
        failures.append("Final release gate report is missing.")
    if not runtime_report_generated_from_validated_runs:
        failures.append("Runtime profile report was not rebuilt in validated-runs mode.")
    if not recognized_manifest_paths:
        failures.append("No recognized validated-run manifests were available for Tier 3 rebuild.")

    warnings: list[str] = []
    if out_of_scope_manifest_paths:
        warnings.append("Out-of-scope validated manifests are present and were excluded from certification counts.")
    if not minimum_inventory_complete:
        warnings.append(
            "Validated artifact inventory is below the required "
            f"{required_runtime_count} runtime + {required_test_lane_count} test lanes "
            "+ 2 backend-distinct migration threshold."
        )

    report_payload = {
        "passed": not failures,
        "summary": {
            "runtime_report_generated_from_validated_runs": runtime_report_generated_from_validated_runs,
            "recognized_manifest_count": len(recognized_manifest_paths),
            "in_scope_validated_manifest_count": len(validated_manifest_paths),
            "out_of_scope_validated_manifest_count": len(out_of_scope_manifest_paths),
            "required_validated_inventory_count": required_inventory_count,
            "validated_inventory_present_count": validated_inventory_present_count,
            "validated_inventory_complete": minimum_inventory_complete,
        },
        "failures": failures,
        "warnings": warnings,
        "details": {
            "validated_execution_report": _relative(validated_path),
            "validated_execution_report_sha256": _sha256_file(validated_path),
            "runtime_profile_report": _relative(runtime_path),
            "runtime_profile_report_sha256": _sha256_file(runtime_path),
            "release_gate_report": _relative(release_gate_path),
            "release_gate_report_sha256": _sha256_file(release_gate_path),
            "final_release_gate_report": _relative(final_gate_path),
            "final_release_gate_report_sha256": _sha256_file(final_gate_path),
            "current_state_report": _relative(current_path),
            "current_state_report_sha256": _sha256_file(current_path),
            "collected_artifact_downloads": _relative(collected_path),
            "collected_artifact_downloads_sha256": _sha256_file(collected_path),
            "recognized_manifest_paths": recognized_manifest_paths,
            "validated_manifest_paths": validated_manifest_paths,
            "out_of_scope_manifest_paths": out_of_scope_manifest_paths,
        },
    }
    _write_report("tier3_evidence_rebuild_report", "Tier 3 Evidence Rebuild Report", report_payload)

    payload.update(
        {
            "passed": not failures,
            "rebuild_from_validated_runs_only": True,
            "runtime_report_generated_from_validated_runs": runtime_report_generated_from_validated_runs,
            "recognized_manifest_count": len(recognized_manifest_paths),
            "in_scope_validated_manifest_count": len(validated_manifest_paths),
            "out_of_scope_validated_manifest_count": len(out_of_scope_manifest_paths),
            "required_validated_inventory_count": required_inventory_count,
            "validated_inventory_present_count": validated_inventory_present_count,
            "validated_inventory_complete": minimum_inventory_complete,
            "signed_release_bundle_count": int(current.get("summary", {}).get("signed_release_bundle_count", 0)),
            "artifact_truthfulness_passed": bool(current.get("summary", {}).get("artifact_truthfulness_passed", False)),
            "validated_execution_report_present": bool(validated),
            "runtime_profile_report_present": bool(runtime),
            "release_gate_report_present": bool(release_gate),
            "final_release_gate_report_present": bool(final_gate),
            "tier3_evidence_rebuild_report_artifact": "docs/compliance/tier3_evidence_rebuild_report.json",
            "tier3_evidence_rebuild_report_sha256": _sha256_file(ROOT / "docs" / "compliance" / "tier3_evidence_rebuild_report.json"),
            "validated_execution_report_artifact": _relative(validated_path),
            "validated_execution_report_sha256": _sha256_file(validated_path),
            "runtime_profile_report_artifact": _relative(runtime_path),
            "runtime_profile_report_sha256": _sha256_file(runtime_path),
            "release_gate_report_artifact": _relative(release_gate_path),
            "release_gate_report_sha256": _sha256_file(release_gate_path),
            "final_release_gate_report_artifact": _relative(final_gate_path),
            "final_release_gate_report_sha256": _sha256_file(final_gate_path),
        }
    )
    return _write_manifest(f"tier3-evidence-py{payload['python_version'].replace('.', '')}", payload)


def main() -> int:
    parser = argparse.ArgumentParser(description="Write validated-run manifests for certification workflows.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    runtime_parser = subparsers.add_parser("runtime-profile")
    runtime_parser.add_argument("--runner", default=None)
    runtime_parser.set_defaults(func=_cmd_runtime_profile)

    lane_parser = subparsers.add_parser("test-lane")
    lane_parser.add_argument("--lane", default=None)
    lane_parser.add_argument("--report", default=None)
    lane_parser.add_argument("--pytest-exit-code", default=None)
    lane_parser.set_defaults(func=_cmd_test_lane)

    migration_parser = subparsers.add_parser("migration-portability")
    migration_parser.add_argument("--report", default=str(ROOT / "docs" / "compliance" / "migration_portability_report.json"))
    migration_parser.set_defaults(func=_cmd_migration_portability)

    evidence_parser = subparsers.add_parser("tier3-evidence")
    evidence_parser.set_defaults(func=_cmd_tier3_evidence)

    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
