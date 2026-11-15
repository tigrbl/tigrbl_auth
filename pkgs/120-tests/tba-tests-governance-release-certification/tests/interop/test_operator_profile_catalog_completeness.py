from __future__ import annotations

from pathlib import Path

import yaml


def test_operator_peer_profile_covers_runtime_operator_targets() -> None:
    root = Path(__file__).resolve().parents[5]
    profile = yaml.safe_load((root / "compliance" / "evidence" / "peer_profiles" / "ops-cli.yaml").read_text(encoding="utf-8"))
    target_to_peer = yaml.safe_load((root / "compliance" / "mappings" / "target-to-peer-profile.yaml").read_text(encoding="utf-8"))
    required = {
        "CLI operator surface",
        "Bootstrap and migration lifecycle",
        "Key lifecycle and JWKS publication",
        "Import/export portability",
        "Release bundle and signature verification",
    }
    assert required <= set(profile["required_targets"])
    for target in required:
        assert target_to_peer[target] == ["ops-cli"]
