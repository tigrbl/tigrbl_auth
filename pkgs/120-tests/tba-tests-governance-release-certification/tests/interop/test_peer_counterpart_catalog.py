from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[5]


def _load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_peer_profiles_reference_known_counterparts() -> None:
    profile_dir = ROOT / "compliance" / "evidence" / "peer_profiles"
    counterpart_dir = ROOT / "compliance" / "evidence" / "peer_counterparts"
    counterparts = {path.stem for path in counterpart_dir.glob("*.yaml")}
    assert counterparts
    for path in sorted(profile_dir.glob("*.yaml")):
        profile = _load_yaml(path)
        counterpart_id = str(profile.get("counterpart_id", ""))
        assert counterpart_id in counterparts, path.name
        assert profile.get("scenario_ids"), path.name
        assert profile.get("preferred_runtime_profile"), path.name


def test_counterpart_catalog_requires_identity_and_runtime_provenance() -> None:
    counterpart_dir = ROOT / "compliance" / "evidence" / "peer_counterparts"
    for path in sorted(counterpart_dir.glob("*.yaml")):
        counterpart = _load_yaml(path)
        assert counterpart.get("required_identity_fields"), path.name
        assert counterpart.get("required_container_fields"), path.name
        assert counterpart.get("required_artifacts"), path.name
