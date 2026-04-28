from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

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


def test_runtime_profile_report_auto_uses_validated_runs_when_validated_manifests_exist(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir(parents=True, exist_ok=True)
    _copy_support_files(repo_root)

    validated_root = repo_root / "dist" / "validated-runs"
    _write_json(
        validated_root / "runtime-base-py310.json",
        {
            "kind": "runtime-profile",
            "matrix_profile": "base",
            "python_version": "3.10",
            "passed": True,
            "runtime_smoke_passed": True,
            "application_probe_passed": True,
            "surface_probe_passed": True,
            "surface_probe_endpoint_count": 4,
            "surface_probe_passed_count": 4,
            "surface_probe_failed_count": 0,
        },
    )

    payload = write_runtime_profile_report(repo_root, deployment=SimpleNamespace(profile="baseline"))

    assert payload["report_mode"] == "validated-runs"
    assert payload["summary"]["source_mode"] == "validated-runs"
    assert payload["summary"]["validated_runtime_cell_count"] == 1
    assert payload["validated_artifact_source"] is None
