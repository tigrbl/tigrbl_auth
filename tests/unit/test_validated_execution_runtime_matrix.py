from __future__ import annotations

import json
from pathlib import Path

from tigrbl_auth.cli.certification_evidence import runtime_identity
from tigrbl_auth.cli.reports import load_validated_execution_status


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _runtime_manifest(profile: str, python_version: str, *, runner: str | None = None, passed: bool = True, serve_check_passed: bool | None = None) -> dict:
    payload = {
        "kind": "runtime-profile",
        "python_version": python_version,
        "matrix_profile": profile,
        "identity": runtime_identity(profile, python_version),
        "environment_identity": {"python_version": python_version, "python_tag": f"py{python_version.replace('.', '')}"},
        "install_substrate_artifact": f"dist/install-substrate/{profile}-py{python_version.replace('.', '')}.json",
        "install_substrate_artifact_sha256": "install-sha",
        "install_substrate_environment_identity": {"python_version": python_version},
        "install_substrate_static_manifest_passed": True,
        "install_substrate_current_profile_import_probe_passed": True,
        "install_substrate_runtime_surface_probe_passed": True,
        "runtime_smoke_artifact": f"dist/runtime-smoke/{profile}-py{python_version.replace('.', '')}.json",
        "runtime_smoke_artifact_sha256": "smoke-sha",
        "runtime_smoke_passed": True,
        "application_probe_passed": True,
        "surface_probe_passed": True,
        "surface_probe_endpoint_count": 4,
        "surface_probe_passed_count": 4,
        "surface_probe_failed_count": 0,
        "passed": passed,
    }
    if runner:
        payload.update(
            {
                "runner": runner,
                "runner_available": True,
                "serve_check_passed": True if serve_check_passed is None else serve_check_passed,
                "serve_check_artifact": f"dist/runtime-smoke/{profile}-{runner}-serve-check.json",
                "serve_check_artifact_sha256": "serve-sha",
            }
        )
    return payload


def test_runtime_matrix_requires_smoke_surface_and_serve_evidence_for_runner_profiles(tmp_path: Path) -> None:
    repo_root = tmp_path
    validated_root = repo_root / "dist" / "validated-runs"
    (repo_root / "docs" / "compliance").mkdir(parents=True, exist_ok=True)

    _write_json(
        validated_root / "runtime-base-py310.json",
        _runtime_manifest("base", "3.10"),
    )
    _write_json(
        validated_root / "runtime-sqlite-uvicorn-py311.json",
        _runtime_manifest("sqlite-uvicorn", "3.11", runner="uvicorn", serve_check_passed=False),
    )

    payload = load_validated_execution_status(repo_root)

    assert payload["validated_artifact_count"] == 2
    assert "base@py3.10" in payload["runtime_matrix_passed"]
    assert "sqlite-uvicorn@py3.11" in payload["runtime_matrix_missing"]
    assert payload["runtime_matrix_passed_count"] == 1
    assert (repo_root / "docs" / "compliance" / "validated_execution_report.json").exists()
