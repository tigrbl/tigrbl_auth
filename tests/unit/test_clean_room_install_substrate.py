from __future__ import annotations

import json
from pathlib import Path

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
