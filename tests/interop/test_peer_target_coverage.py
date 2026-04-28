from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def _load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _retained_targets() -> list[str]:
    scope = _load_yaml(ROOT / "compliance" / "targets" / "certification_scope.yaml")
    return [
        str(entry.get("label"))
        for entry in scope.get("targets", [])
        if str(entry.get("scope_bucket")) != "out-of-scope/deferred"
    ]


def test_every_retained_target_has_known_peer_mapping() -> None:
    mapping = _load_yaml(ROOT / "compliance" / "mappings" / "target-to-peer-profile.yaml")
    profiles = {path.stem for path in (ROOT / "compliance" / "evidence" / "peer_profiles").glob("*.yaml")}
    missing = [target for target in _retained_targets() if target not in mapping]
    assert missing == []
    unknown = [
        (target, profile)
        for target, refs in mapping.items()
        if target in _retained_targets()
        for profile in refs
        if profile not in profiles
    ]
    assert unknown == []


def test_peer_profiles_and_reverse_mapping_stay_in_sync() -> None:
    mapping = _load_yaml(ROOT / "compliance" / "mappings" / "target-to-peer-profile.yaml")
    profiles = {
        path.stem: _load_yaml(path)
        for path in (ROOT / "compliance" / "evidence" / "peer_profiles").glob("*.yaml")
    }
    for profile_name, profile in profiles.items():
        for target in profile.get("required_targets", []) or []:
            assert profile_name in list(mapping.get(target, [])), (profile_name, target)
