from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from generate_capability_registry import build_registry  # noqa: E402


def test_capability_family_registry_matches_live_packages() -> None:
    recorded = json.loads(
        (ROOT / "pkgs/40-capabilities/capability-families.json").read_text(
            encoding="utf-8"
        )
    )
    assert recorded == build_registry()


def test_canonical_capability_packages_have_one_implementation() -> None:
    registry = build_registry()
    for package in registry["capabilities"]:
        if package["compatibility_aggregator"]:
            continue
        assert len(package["implementations"]) == 1, package["package"]
