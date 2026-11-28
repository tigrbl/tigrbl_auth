from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]


def test_external_handoff_template_covers_every_peer_profile() -> None:
    template_root = ROOT / "dist" / "tier4-external-handoff"
    manifest = json.loads((template_root / "external-root-template.json").read_text(encoding="utf-8"))
    profile_dir = ROOT / "compliance" / "evidence" / "peer_profiles"
    profiles = sorted(path.stem for path in profile_dir.glob("*.yaml"))
    assert manifest["profile_count"] == len(profiles)
    assert sorted(item["profile"] for item in manifest["profiles"]) == profiles


def test_each_external_handoff_profile_has_fill_in_templates() -> None:
    template_root = ROOT / "dist" / "tier4-external-handoff"
    for profile_dir in sorted(path for path in template_root.iterdir() if path.is_dir()):
        assert (profile_dir / "manifest.template.yaml").exists(), profile_dir.name
        assert (profile_dir / "result.template.yaml").exists(), profile_dir.name
        assert (profile_dir / "reproduction.template.md").exists(), profile_dir.name
        assert (profile_dir / "CHECKLIST.md").exists(), profile_dir.name
        assert (profile_dir / "required-artifact-placeholders").exists(), profile_dir.name
