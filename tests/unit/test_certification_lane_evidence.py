from __future__ import annotations

import json
from pathlib import Path

from scripts.collect_validated_artifact_downloads import collect_validated_artifact_downloads
from tests.lanes import test_file_requires_runtime_stack as file_requires_runtime_stack
from tigrbl_auth.cli.certification_evidence import lane_identity
from tigrbl_auth.cli.reports import load_validated_execution_status


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _lane_manifest(lane: str, python_version: str, *, tests_collected: int = 7, passed: bool = True) -> dict:
    return {
        "kind": "test-lane",
        "lane": lane,
        "python_version": python_version,
        "identity": lane_identity(lane, python_version),
        "environment_identity": {"python_version": python_version, "python_tag": f"py{python_version.replace('.', '')}"},
        "install_substrate_artifact": f"dist/install-substrate/test-{lane}-py{python_version.replace('.', '')}.json",
        "install_substrate_artifact_sha256": "install-sha",
        "install_substrate_environment_identity": {"python_version": python_version},
        "install_substrate_static_manifest_passed": True,
        "install_substrate_current_profile_import_probe_passed": True,
        "install_substrate_runtime_surface_probe_passed": True,
        "pytest_report_artifact": f"dist/test-reports/{lane}-py{python_version.replace('.', '')}.json",
        "pytest_report_sha256": "pytest-sha",
        "pytest_report_present": True,
        "pytest_exit_code": 0,
        "pytest_report_exit_code": 0,
        "tests_collected": tests_collected,
        "tests_total": tests_collected,
        "passed": passed,
    }


def test_test_lane_requires_pytest_report_and_collected_tests(tmp_path: Path) -> None:
    repo_root = tmp_path
    validated_root = repo_root / "dist" / "validated-runs"
    (repo_root / "docs" / "compliance").mkdir(parents=True, exist_ok=True)

    _write_json(
        validated_root / "test-core-py310.json",
        {
            **_lane_manifest("core", "3.10"),
            "pytest_report_artifact": None,
            "pytest_report_sha256": None,
            "pytest_report_present": False,
        },
    )
    _write_json(
        validated_root / "test-integration-py311.json",
        _lane_manifest("integration", "3.11", tests_collected=0),
    )
    _write_json(
        validated_root / "test-conformance-py312.json",
        _lane_manifest("conformance", "3.12", tests_collected=7),
    )

    payload = load_validated_execution_status(repo_root)

    assert "core@py3.10" in payload["test_lane_missing"]
    assert "integration@py3.11" in payload["test_lane_missing"]
    assert "conformance@py3.12" in payload["test_lane_passed"]
    assert payload["test_lane_passed_count"] == 1


def test_collect_validated_artifact_downloads_preserves_test_reports(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir(parents=True, exist_ok=True)
    download_root = tmp_path / "downloads"

    _write_json(
        download_root / "validated-py310-test-core" / "dist" / "test-reports" / "py310-test-core.json",
        {"exitcode": 0, "summary": {"total": 4, "collected": 4, "passed": 4}},
    )
    _write_json(
        download_root / "validated-py311-test-core" / "dist" / "test-reports" / "py311-test-core.json",
        {"exitcode": 0, "summary": {"total": 5, "collected": 5, "passed": 5}},
    )

    payload = collect_validated_artifact_downloads(repo_root, download_root=download_root)

    assert payload["passed"] is True
    assert payload["artifact_count"] == 2
    assert payload["test_report_file_count"] == 2
    py310_report = repo_root / "dist" / "test-reports" / "collected" / "validated-py310-test-core" / "py310-test-core.json"
    py311_report = repo_root / "dist" / "test-reports" / "collected" / "validated-py311-test-core" / "py311-test-core.json"
    assert json.loads(py310_report.read_text(encoding="utf-8"))["summary"]["total"] == 4
    assert json.loads(py311_report.read_text(encoding="utf-8"))["summary"]["total"] == 5


def test_validated_execution_excludes_out_of_scope_lane_manifests_from_certification_counts(tmp_path: Path) -> None:
    repo_root = tmp_path
    validated_root = repo_root / "dist" / "validated-runs"
    (repo_root / "docs" / "compliance").mkdir(parents=True, exist_ok=True)

    _write_json(
        validated_root / "test-core-py313.json",
        _lane_manifest("core", "3.13", tests_collected=8),
    )
    _write_json(
        validated_root / "test-core-py310.json",
        _lane_manifest("core", "3.10", tests_collected=4),
    )

    payload = load_validated_execution_status(repo_root)

    assert payload["validated_artifact_count"] == 1
    assert payload["out_of_scope_validated_artifact_count"] == 1
    assert payload["test_lane_passed_count"] == 1
    assert payload["out_of_scope_validated_manifests"][0]["identity"] == "core@py3.13"


def test_runtime_stack_detection_catches_dynamic_import_targets(tmp_path: Path) -> None:
    path = tmp_path / "test_dynamic_import.py"
    path.write_text(
        "import importlib\n\n"
        "def test_runtime_import():\n"
        "    importlib.import_module('tigrbl_auth.standards.oauth2.introspection')\n",
        encoding="utf-8",
    )

    assert file_requires_runtime_stack(str(path)) is True
