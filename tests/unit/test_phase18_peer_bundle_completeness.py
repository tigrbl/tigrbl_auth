from __future__ import annotations

import shutil
from pathlib import Path

from tigrbl_auth.cli.reports import verify_peer_bundle_completeness


ROOT = Path(__file__).resolve().parents[2]


def _copy_tree(src: Path, dst: Path) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    for path in src.iterdir():
        target = dst / path.name
        if path.is_dir():
            shutil.copytree(path, target)
        else:
            shutil.copy2(path, target)


def test_peer_bundle_completeness_requires_preserved_bundle_for_every_declared_profile(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    profile_dir = repo_root / "compliance" / "evidence" / "peer_profiles"
    bundle_dir = repo_root / "compliance" / "evidence" / "tier4" / "bundles"
    docs_dir = repo_root / "docs" / "compliance"
    _copy_tree(ROOT / "compliance" / "evidence" / "peer_profiles", profile_dir)
    bundle_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)

    initial = verify_peer_bundle_completeness(repo_root)
    assert initial["passed"] is False
    assert initial["summary"]["declared_peer_profile_count"] == 16
    assert initial["summary"]["preserved_bundle_count"] == 0
    assert initial["summary"]["missing_bundle_count"] == 16

    _copy_tree(ROOT / "compliance" / "evidence" / "tier4" / "bundles", bundle_dir)
    complete = verify_peer_bundle_completeness(repo_root)
    assert complete["passed"] is True
    assert complete["summary"]["declared_peer_profile_count"] == 16
    assert complete["summary"]["preserved_bundle_count"] == 16
    assert complete["summary"]["missing_bundle_count"] == 0
    details = {row["profile"]: row for row in complete["details"]}
    assert details["browser"]["bundle_present"] is True
    assert details["browser"]["status"] == "external-preserved-failed"
    assert details["browser"]["has_reproduction"] is True
    assert details["browser"]["validation_failure_count"] > 0
