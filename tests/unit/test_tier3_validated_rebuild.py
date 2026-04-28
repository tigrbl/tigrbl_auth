from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

from scripts.collect_validated_artifact_downloads import collect_validated_artifact_downloads
from tigrbl_auth.cli.certification_evidence import runtime_identity
from tigrbl_auth.cli.reports import load_validated_execution_status
from tigrbl_auth.cli.runtime import write_runtime_profile_report

ROOT = Path(__file__).resolve().parents[2]


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _copy_support_files(dst_root: Path) -> None:
    for rel in [
        "pyproject.toml",
        "tox.ini",
        ".github/workflows/ci-install-profiles.yml",
        ".github/workflows/ci-release-gates.yml",
        "constraints/base.txt",
        "constraints/test.txt",
        "constraints/runner-uvicorn.txt",
        "constraints/runner-hypercorn.txt",
        "constraints/runner-tigrcorn.txt",
    ]:
        src = ROOT / rel
        dst = dst_root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")


def _runtime_manifest(profile: str, python_version: str, *, runner: str | None = None) -> dict:
    payload = {
        "kind": "runtime-profile",
        "matrix_profile": profile,
        "python_version": python_version,
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
        "passed": True,
    }
    if runner:
        payload.update(
            {
                "runner": runner,
                "runner_available": True,
                "serve_check_passed": True,
                "serve_check_artifact": f"dist/runtime-smoke/{profile}-{runner}-serve-check.json",
                "serve_check_artifact_sha256": "serve-sha",
            }
        )
    return payload


def test_tier3_validated_rebuild_requires_validated_run_rebuild_fields(tmp_path: Path) -> None:
    repo_root = tmp_path
    validated_root = repo_root / "dist" / "validated-runs"

    _write_json(
        validated_root / "tier3-evidence-py311.json",
        {
            "kind": "tier3-evidence",
            "python_version": "3.11",
            "passed": True,
            "rebuild_from_validated_runs_only": True,
            "runtime_report_generated_from_validated_runs": True,
            "validated_execution_report_present": True,
            "runtime_profile_report_present": True,
            "recognized_manifest_count": 6,
        },
    )
    payload = load_validated_execution_status(repo_root)
    assert payload["tier3_evidence_rebuilt_from_validated_runs"] is True

    _write_json(
        validated_root / "tier3-evidence-py311.json",
        {
            "kind": "tier3-evidence",
            "python_version": "3.11",
            "passed": True,
            "rebuild_from_validated_runs_only": True,
            "runtime_report_generated_from_validated_runs": False,
            "validated_execution_report_present": True,
            "runtime_profile_report_present": True,
            "recognized_manifest_count": 6,
        },
    )
    payload = load_validated_execution_status(repo_root)
    assert payload["tier3_evidence_rebuilt_from_validated_runs"] is False


def test_runtime_profile_report_can_be_rebuilt_from_validated_run_manifests(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir(parents=True, exist_ok=True)
    _copy_support_files(repo_root)

    validated_root = repo_root / "dist" / "validated-runs"
    _write_json(repo_root / "dist" / "validated-runs" / "collected-artifact-downloads.json", {"passed": True, "artifact_count": 2})
    _write_json(
        validated_root / "runtime-base-py310.json",
        _runtime_manifest("base", "3.10"),
    )
    _write_json(
        validated_root / "runtime-sqlite-uvicorn-py310.json",
        _runtime_manifest("sqlite-uvicorn", "3.10", runner="uvicorn"),
    )

    payload = write_runtime_profile_report(
        repo_root,
        deployment=SimpleNamespace(profile="baseline"),
        report_mode="validated-runs",
    )

    assert payload["report_mode"] == "validated-runs"
    assert payload["summary"]["source_mode"] == "validated-runs"
    assert payload["summary"]["required_runtime_cell_count"] == 14
    assert payload["summary"]["validated_runtime_cell_count"] == 2
    assert payload["summary"]["validated_runtime_cell_passed_count"] == 2
    assert payload["validated_artifact_source"] == "dist/validated-runs/collected-artifact-downloads.json"
    assert (repo_root / "docs" / "compliance" / "runtime_profile_report.json").exists()


def test_collect_validated_artifact_downloads_fails_on_empty_artifact_directories(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir(parents=True, exist_ok=True)
    download_root = tmp_path / "downloads"
    (download_root / "validated-empty-artifact").mkdir(parents=True, exist_ok=True)

    payload = collect_validated_artifact_downloads(repo_root, download_root=download_root)

    assert payload["passed"] is False
    assert payload["artifact_count"] == 1
    assert payload["empty_artifact_count"] == 1
    assert payload["empty_artifacts"] == ["validated-empty-artifact"]
