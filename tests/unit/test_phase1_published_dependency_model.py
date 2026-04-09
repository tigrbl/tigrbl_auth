from __future__ import annotations

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 fallback
    import tomli as tomllib
from pathlib import Path

from tigrbl_auth.cli.reports import _dependency_artifact_paths, generate_state_reports


ROOT = Path(__file__).resolve().parents[2]


def _load_pyproject() -> dict:
    return tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))


def test_phase1_pyproject_uses_published_pins_and_extras():
    manifest = _load_pyproject()
    project = manifest["project"]
    dependencies = set(project["dependencies"])
    extras = project["optional-dependencies"]

    assert "tigrbl==0.3.15" in dependencies
    assert "swarmauri_core==0.9.2" in dependencies
    assert "swarmauri_standard==0.9.2" in dependencies
    assert "swarmauri_tokens_jwt==0.3.0.dev31" in dependencies
    assert "swarmauri_crypto_jwe==0.2.0.dev40" in dependencies

    assert set({"postgres", "sqlite", "uvicorn", "hypercorn", "tigrcorn", "servers"}) <= set(extras)
    assert extras["uvicorn"] == ["uvicorn[standard]==0.41.0"]
    assert "sqlalchemy[asyncio]==2.0.48" in dependencies
    assert "pydantic[email]==2.12.5" in dependencies
    assert extras["hypercorn"] == ["hypercorn==0.18.0"]
    assert extras["tigrcorn"] == ["tigrcorn==0.3.8; python_version >= '3.11'"]
    assert "tigrcorn==0.3.8; python_version >= '3.11'" in extras["servers"]


def test_phase1_workspace_sources_removed_and_provenance_artifacts_exist():
    manifest = _load_pyproject()
    assert "uv" not in manifest.get("tool", {}) or "sources" not in manifest["tool"].get("uv", {})

    required = {
        "constraints/base.txt",
        "constraints/runner-uvicorn.txt",
        "constraints/runner-hypercorn.txt",
        "constraints/runner-tigrcorn.txt",
        "constraints/dependency-lock.json",
        "docs/runbooks/INSTALLATION_PROFILES.md",
        "docs/runbooks/CLEAN_CHECKOUT_REPRO.md",
        ".github/workflows/ci-install-profiles.yml",
        "scripts/verify_clean_room_install_substrate.py",
        "scripts/run_certification_lane.py",
    }
    assert required <= set(_dependency_artifact_paths(ROOT))

    dockerfile = (ROOT / "Dockerfile").read_text(encoding="utf-8")
    assert "./pkgs/" not in dockerfile
    assert "constraints/base.txt" in dockerfile


def test_phase1_state_report_tracks_dependency_model_checkpoint():
    payload = generate_state_reports(ROOT)
    summary = payload["current_state"]

    assert summary["workspace_sources_present"] is False
    assert summary["dependency_lock_manifest_present"] is True
    assert summary["install_profile_workflow_present"] is True
    assert summary["tigrcorn_extra_placeholder"] is False
    assert summary["tigrcorn_pin_committed"] is True
    assert summary["runtime_profile_placeholder_supported_runner_count"] == 0
    assert summary["runtime_profile_declared_ci_install_probe_complete"] is True
    assert summary["install_substrate_report_present"] is True
    assert summary["install_substrate_manifest_passed"] is True
    assert summary["install_substrate_tox_pip_check_complete"] is True
    assert summary["install_substrate_tox_import_probe_complete"] is True
    assert summary["migration_portability_passed"] is True
    assert summary["base_dependency_count"] >= 12
    assert summary["base_exact_pinned_dependency_count"] == summary["base_dependency_count"]
