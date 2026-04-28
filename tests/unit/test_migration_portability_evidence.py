from __future__ import annotations

import json
from pathlib import Path

from tigrbl_auth.cli.certification_evidence import (
    migration_identity,
    validated_migration_backend_manifest_passed,
    validated_migration_manifest_passed,
)
from tigrbl_auth.cli.reports import load_validated_execution_status


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _migration_manifest(*, python_version: str = "3.11", passed_backends: list[str] | None = None) -> dict:
    passed_backends = list(passed_backends or ["sqlite", "postgres"])
    backend_results = {}
    for backend in ["sqlite", "postgres"]:
        backend_results[backend] = {
            "available": backend in passed_backends,
            "passed": backend in passed_backends,
            "upgrade_passed": backend in passed_backends,
            "downgrade_passed": backend in passed_backends,
            "reapply_passed": backend in passed_backends,
            "artifacts": {
                "upgrade": f"dist/migration-portability/{backend}/upgrade.json",
                "downgrade": f"dist/migration-portability/{backend}/downgrade.json",
                "reapply": f"dist/migration-portability/{backend}/reapply.json",
            },
            "expected_head_revision": "0007_browser_session_cookie_and_auth_code_linkage",
            "head_revision_after_upgrade": "0007_browser_session_cookie_and_auth_code_linkage",
            "downgraded_revision": "0007_browser_session_cookie_and_auth_code_linkage",
            "head_revision_after_downgrade": "0006_previous",
            "head_revision_after_reapply": "0007_browser_session_cookie_and_auth_code_linkage",
        }
    return {
        "kind": "migration-portability",
        "python_version": python_version,
        "identity": migration_identity("migration-portability", python_version),
        "environment_identity": {"python_version": python_version, "python_tag": f"py{python_version.replace('.', '')}"},
        "install_substrate_artifact": f"dist/install-substrate/migration-portability-py{python_version.replace('.', '')}.json",
        "install_substrate_artifact_sha256": "install-sha",
        "install_substrate_environment_identity": {"python_version": python_version},
        "install_substrate_static_manifest_passed": True,
        "install_substrate_current_profile_import_probe_passed": True,
        "install_substrate_runtime_surface_probe_passed": True,
        "backends": ["sqlite", "postgres"],
        "required_backends": ["sqlite", "postgres"],
        "passed_backends": passed_backends,
        "backend_manifests": [
            {
                "backend": backend,
                "path": f"dist/validated-runs/migration-portability-{backend}-py{python_version.replace('.', '')}.json",
                "sha256": f"{backend}-sha",
                "passed": backend in passed_backends,
            }
            for backend in ["sqlite", "postgres"]
        ],
        "backend_results": backend_results,
        "revision_inventory": [
            {"revision": "0006_previous", "down_revision": "0005_previous"},
            {"revision": "0007_browser_session_cookie_and_auth_code_linkage", "down_revision": "0006_previous"},
        ],
        "head_revision": "0007_browser_session_cookie_and_auth_code_linkage",
        "expected_head_revision": "0007_browser_session_cookie_and_auth_code_linkage",
        "downgrade_target_revision": "0006_previous",
        "pytest_report_artifact": f"dist/test-reports/migration-portability-py{python_version.replace('.', '')}.json",
        "pytest_report_sha256": "pytest-sha",
        "pytest_exit_code": 0,
        "passed": passed_backends == ["sqlite", "postgres"],
    }


def _migration_backend_manifest(backend: str, *, python_version: str = "3.11", passed: bool = True) -> dict:
    return {
        "kind": "migration-portability-backend",
        "backend": backend,
        "python_version": python_version,
        "identity": migration_identity(f"migration-portability-{backend}", python_version),
        "environment_identity": {"python_version": python_version, "python_tag": f"py{python_version.replace('.', '')}"},
        "install_substrate_artifact": f"dist/install-substrate/migration-portability-py{python_version.replace('.', '')}.json",
        "install_substrate_artifact_sha256": "install-sha",
        "install_substrate_environment_identity": {"python_version": python_version},
        "install_substrate_static_manifest_passed": True,
        "install_substrate_current_profile_import_probe_passed": True,
        "install_substrate_runtime_surface_probe_passed": True,
        "available": passed,
        "passed": passed,
        "upgrade_passed": passed,
        "downgrade_passed": passed,
        "reapply_passed": passed,
        "artifacts": {
            "upgrade": f"dist/migration-portability/{backend}/upgrade.json",
            "downgrade": f"dist/migration-portability/{backend}/downgrade.json",
            "reapply": f"dist/migration-portability/{backend}/reapply.json",
        },
        "artifact_sha256": {"upgrade": "u-sha", "downgrade": "d-sha", "reapply": "r-sha"},
        "expected_head_revision": "0007_browser_session_cookie_and_auth_code_linkage",
        "downgrade_target_revision": "0006_previous",
        "downgraded_revision": "0007_browser_session_cookie_and_auth_code_linkage",
        "head_revision_after_upgrade": "0007_browser_session_cookie_and_auth_code_linkage",
        "head_revision_after_downgrade": "0006_previous",
        "head_revision_after_reapply": "0007_browser_session_cookie_and_auth_code_linkage",
    }


def test_migration_manifest_requires_both_backends_and_revision_inventory() -> None:
    payload = _migration_manifest()
    assert validated_migration_manifest_passed(payload) is True
    assert validated_migration_backend_manifest_passed(_migration_backend_manifest("sqlite")) is True
    assert validated_migration_backend_manifest_passed(_migration_backend_manifest("postgres")) is True

    missing_postgres = _migration_manifest(passed_backends=["sqlite"])
    assert validated_migration_manifest_passed(missing_postgres) is False

    missing_revision_target = _migration_manifest()
    missing_revision_target["downgrade_target_revision"] = None
    assert validated_migration_manifest_passed(missing_revision_target) is False


def test_validated_execution_uses_strict_migration_manifest_contract(tmp_path: Path) -> None:
    repo_root = tmp_path
    validated_root = repo_root / "dist" / "validated-runs"
    (repo_root / "docs" / "compliance").mkdir(parents=True, exist_ok=True)

    _write_json(validated_root / "migration-portability-py311.json", _migration_manifest())
    _write_json(validated_root / "migration-portability-sqlite-py311.json", _migration_backend_manifest("sqlite"))
    _write_json(validated_root / "migration-portability-postgres-py311.json", _migration_backend_manifest("postgres"))
    payload = load_validated_execution_status(repo_root)
    assert payload["migration_portability_passed"] is True

    _write_json(validated_root / "migration-portability-py311.json", _migration_manifest(passed_backends=["sqlite"]))
    _write_json(validated_root / "migration-portability-postgres-py311.json", _migration_backend_manifest("postgres", passed=False))
    payload = load_validated_execution_status(repo_root)
    assert payload["migration_portability_passed"] is False


def test_validated_execution_prefers_strongest_backend_manifest_per_backend(tmp_path: Path) -> None:
    repo_root = tmp_path
    validated_root = repo_root / "dist" / "validated-runs"
    (repo_root / "docs" / "compliance").mkdir(parents=True, exist_ok=True)

    _write_json(validated_root / "migration-portability-py311.json", _migration_manifest())
    _write_json(validated_root / "migration-portability-sqlite-py311.json", _migration_backend_manifest("sqlite"))
    _write_json(validated_root / "migration-portability-postgres-py311.json", _migration_backend_manifest("postgres"))
    _write_json(validated_root / "migration-portability-sqlite-py312.json", _migration_backend_manifest("sqlite", python_version="3.12", passed=False))
    _write_json(validated_root / "migration-portability-postgres-py312.json", _migration_backend_manifest("postgres", python_version="3.12", passed=False))

    payload = load_validated_execution_status(repo_root)

    assert payload["migration_portability_passed"] is True
