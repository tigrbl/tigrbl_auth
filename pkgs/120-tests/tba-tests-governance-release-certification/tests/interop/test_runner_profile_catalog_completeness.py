from __future__ import annotations

from pathlib import Path

import yaml


def test_runner_peer_profiles_cover_all_supported_runner_targets() -> None:
    root = Path(__file__).resolve().parents[5]
    peer_dir = root / "compliance" / "evidence" / "peer_profiles"
    target_to_peer = yaml.safe_load((root / "compliance" / "mappings" / "target-to-peer-profile.yaml").read_text(encoding="utf-8"))
    profiles = {path.stem: yaml.safe_load(path.read_text(encoding="utf-8")) for path in peer_dir.glob("runner-*.yaml")}

    assert set(profiles) == {"runner-uvicorn", "runner-hypercorn", "runner-tigrcorn"}
    assert target_to_peer["Runner profile: Uvicorn"] == ["runner-uvicorn"]
    assert target_to_peer["Runner profile: Hypercorn"] == ["runner-hypercorn"]
    assert target_to_peer["Runner profile: Tigrcorn"] == ["runner-tigrcorn"]
    for profile in profiles.values():
        assert profile["counterpart_id"]
        assert profile["required_targets"]
