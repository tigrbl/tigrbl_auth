from __future__ import annotations

import json
import sys
from pathlib import Path

from tigrbl_auth.cli import install_substrate
from tigrbl_auth.cli.install_substrate import build_install_substrate_report
from tigrbl_auth.cli.reports import _dependency_artifact_paths, generate_state_reports

ROOT = Path(__file__).resolve().parents[2]


def test_install_substrate_report_static_manifest_passes_and_tracks_profile_counts() -> None:
    payload = build_install_substrate_report(ROOT)
    summary = payload["summary"]

    assert summary["static_manifest_passed"] is True
    assert summary["declared_runtime_matrix_env_count"] == 14
    assert summary["declared_test_lane_env_count"] == 15
    assert summary["declared_certification_tox_env_count"] == 33
    assert summary["tox_section_template_count"] == 14
    assert summary["tox_envs_declare_pip_check"] is True
    assert summary["tox_envs_declare_install_probe"] is True
    assert summary["install_profiles_runtime_env_present_count"] == 14
    assert summary["release_gates_runtime_env_present_count"] == 14
    assert summary["release_gates_test_lane_env_present_count"] == 15
    assert summary["release_gates_extra_env_present_count"] == 2


def test_install_substrate_warns_when_sibling_supported_pythons_are_absent(monkeypatch) -> None:
    current_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    if current_version not in install_substrate.SUPPORTED_PYTHON_VERSIONS:
        return

    monkeypatch.setattr(
        install_substrate,
        "_detect_supported_pythons",
        lambda: [
            {
                "version": version,
                "available": version == current_version,
                "path": sys.executable if version == current_version else None,
                "source": "current-interpreter" if version == current_version else None,
            }
            for version in install_substrate.SUPPORTED_PYTHON_VERSIONS
        ],
    )

    payload = build_install_substrate_report(ROOT, execute_import_probes=False)

    assert payload["passed"] is True
    assert not any("full supported interpreter matrix" in item for item in payload["failures"])
    assert any("does not provide supported interpreter binaries" in item for item in payload["warnings"])


def test_dependency_artifact_paths_include_install_substrate_verifier() -> None:
    assert "scripts/verify_clean_room_install_substrate.py" in _dependency_artifact_paths(ROOT)


def test_generate_state_reports_tracks_install_substrate_checkpoint() -> None:
    payload = generate_state_reports(ROOT)
    summary = payload["current_state"]

    assert summary["install_substrate_report_present"] is True
    assert summary["install_substrate_manifest_passed"] is True
    assert summary["install_substrate_tox_env_count"] == 33
    assert summary["install_substrate_tox_pip_check_complete"] is True
    assert summary["install_substrate_tox_import_probe_complete"] is True
    assert summary["install_substrate_expected_supported_python_count"] == 3


def test_dependency_lock_manifest_covers_certification_lane_profiles() -> None:
    payload = json.loads((ROOT / "constraints" / "dependency-lock.json").read_text(encoding="utf-8"))
    profiles = set((payload.get("install_profiles") or {}).keys())
    assert {
        "test-core",
        "test-integration",
        "test-conformance",
        "test-security-negative",
        "test-interop",
        "test-extension",
        "migration-portability",
        "final-certification",
    } <= profiles


def test_detect_supported_pythons_counts_current_certification_interpreter(monkeypatch) -> None:
    current_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    if current_version not in install_substrate.SUPPORTED_PYTHON_VERSIONS:
        return

    monkeypatch.setattr(install_substrate.shutil, "which", lambda _name: None)

    detections = install_substrate._detect_supported_pythons()
    current_detection = next(item for item in detections if item["version"] == current_version)

    assert current_detection["available"] is True
    assert current_detection["path"] == sys.executable
    assert current_detection["source"] == "current-interpreter"


def test_runtime_surface_probe_resolves_split_package_source_roots() -> None:
    results = install_substrate._runtime_surface_probe(ROOT)

    assert results
    assert all(item["passed"] for item in results)
    assert {item["module"] for item in results} >= {
        "tigrbl_identity_server.api.app",
        "tigrbl_auth.app",
    }
