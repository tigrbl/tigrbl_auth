from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[5]


def _load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_candidate_bundle_layout_exists_for_each_peer_profile() -> None:
    profile_dir = ROOT / "compliance" / "evidence" / "peer_profiles"
    candidate_root = ROOT / "compliance" / "evidence" / "tier4" / "candidates"
    for path in sorted(profile_dir.glob("*.yaml")):
        candidate_dir = candidate_root / path.stem
        assert candidate_dir.exists(), path.stem
        assert (candidate_dir / "manifest.yaml").exists(), path.stem
        assert (candidate_dir / "mapping.yaml").exists(), path.stem
        assert (candidate_dir / "peer-profile.yaml").exists(), path.stem
        assert (candidate_dir / "peer-artifacts").exists(), path.stem


def test_peer_matrix_report_is_present() -> None:
    report = ROOT / "docs" / "compliance" / "peer_matrix_report.json"
    assert report.exists()
    payload = _load_yaml(report)
    assert payload["summary"]["profile_count"] >= 1
