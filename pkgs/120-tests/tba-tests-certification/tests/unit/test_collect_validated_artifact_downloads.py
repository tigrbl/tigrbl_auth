from __future__ import annotations

import json
from pathlib import Path

from scripts.collect_validated_artifact_downloads import collect_validated_artifact_downloads


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def test_collect_validated_artifact_downloads_preserves_runtime_smoke_per_artifact(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir(parents=True, exist_ok=True)
    download_root = tmp_path / "downloads"

    _write_json(
        download_root / "validated-py310-base" / "dist" / "validated-runs" / "runtime-base-py310.json",
        {"kind": "runtime-profile", "matrix_profile": "base", "python_version": "3.10", "passed": True},
    )
    _write_json(
        download_root / "validated-py310-base" / "dist" / "runtime-smoke" / "base-base.json",
        {"python": "3.10.14"},
    )
    _write_json(
        download_root / "validated-py311-base" / "dist" / "validated-runs" / "runtime-base-py311.json",
        {"kind": "runtime-profile", "matrix_profile": "base", "python_version": "3.11", "passed": True},
    )
    _write_json(
        download_root / "validated-py311-base" / "dist" / "runtime-smoke" / "base-base.json",
        {"python": "3.11.9"},
    )

    payload = collect_validated_artifact_downloads(repo_root, download_root=download_root)

    assert payload["passed"] is True
    assert payload["artifact_count"] == 2
    assert payload["validated_manifest_count"] == 2
    assert payload["runtime_smoke_file_count"] == 2
    assert (repo_root / "dist" / "validated-runs" / "runtime-base-py310.json").exists()
    assert (repo_root / "dist" / "validated-runs" / "runtime-base-py311.json").exists()
    py310_smoke = repo_root / "dist" / "runtime-smoke" / "collected" / "validated-py310-base" / "base-base.json"
    py311_smoke = repo_root / "dist" / "runtime-smoke" / "collected" / "validated-py311-base" / "base-base.json"
    assert json.loads(py310_smoke.read_text(encoding="utf-8"))["python"] == "3.10.14"
    assert json.loads(py311_smoke.read_text(encoding="utf-8"))["python"] == "3.11.9"
    assert (repo_root / "dist" / "validated-runs" / "collected-artifact-downloads.json").exists()
