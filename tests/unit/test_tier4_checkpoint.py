from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _repo_copy(src: Path, dst: Path) -> Path:
    shutil.copytree(
        src,
        dst,
        ignore=shutil.ignore_patterns(
            ".git",
            ".pytest-tmp*",
            ".test-tmp-*",
            ".codex-tmp-*",
            ".pytest_cache*",
            ".uv-cache",
            ".uv-cache-local",
            ".uv-project-env",
            ".venv",
            ".benchmarks",
            ".operator-state",
            ".operator-state-test",
            ".tmp",
            ".tox",
            ".artifacts",
            ".uv-python",
            "dist",
            "__pycache__",
            "*.pyc",
            "*.db",
            "*.sqlite",
        ),
    )
    return dst


def test_require_full_boundary_fails_closed_for_nonqualifying_fixture_root(tmp_path: Path) -> None:
    repo_copy = _repo_copy(ROOT, tmp_path / "repo")
    fixture_root = Path("dist") / "tier4-external-root-fixtures" / "capability-fixtures"

    stage = subprocess.run(
        [
            sys.executable,
            "scripts/stage_tier4_external_root_fixtures.py",
            "--output-root",
            str(fixture_root),
        ],
        cwd=repo_copy,
        check=True,
        capture_output=True,
        text=True,
    )
    assert stage.returncode == 0

    materialize = subprocess.run(
        [
            sys.executable,
            "scripts/materialize_tier4_peer_evidence.py",
            "--external-root",
            str(fixture_root),
            "--require-full-boundary",
        ],
        cwd=repo_copy,
        capture_output=True,
        text=True,
    )
    assert materialize.returncode == 1, materialize.stdout + materialize.stderr

    payload = json.loads((repo_copy / "docs" / "compliance" / "peer_matrix_report.json").read_text(encoding="utf-8"))
    summary = payload["summary"]
    assert summary["supported_peer_profile_count"] == 16
    assert summary["external_bundle_count"] == 16
    assert summary["valid_external_bundle_count"] == 0
    assert summary["invalid_external_bundle_count"] == 16
    assert summary["missing_external_bundle_count"] == 0
    assert summary["strict_independent_claims_ready"] is False
