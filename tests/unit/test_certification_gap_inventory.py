from __future__ import annotations

import json
import re
from pathlib import Path

from scripts.generate_certification_gap_inventory import build_inventory, write_inventory


ROOT = Path(__file__).resolve().parents[2]


def test_certification_gap_inventory_reflects_live_registry(tmp_path: Path) -> None:
    inventory = build_inventory(ROOT)
    registry = json.loads((ROOT / ".ssot" / "registry.json").read_text(encoding="utf-8"))

    assert inventory["registry"]["counts"]["features"] == len(registry["features"])
    assert inventory["registry"]["counts"]["profiles"] == len(registry["profiles"])
    assert inventory["registry"]["counts"]["tests"] == len(registry["tests"])
    assert inventory["registry"]["validation_passed"] is True
    assert inventory["current_gaps"]["claims_without_tests"] == []
    assert inventory["current_gaps"]["claims_without_evidence"] == []
    assert inventory["current_gaps"]["tests_without_evidence"] == []

    current_feature_ids = {
        row["id"] for row in inventory["current_gaps"]["current_partial_or_absent_features"]
    }
    assert current_feature_ids == set()

    outputs = write_inventory(inventory, report_dir=tmp_path)
    assert outputs["json"].endswith("certification-gap-inventory.json")
    assert outputs["markdown"].endswith("certification-gap-inventory.md")


def test_certification_gap_inventory_uses_capability_scoped_track_names() -> None:
    inventory = build_inventory(ROOT)

    for track in inventory["delivery_tracks"]:
        text = " ".join(str(value) for value in track.values()).lower()
        assert "phase" not in text
        assert "step" not in text


def test_certification_gap_inventory_omits_chronology_scoped_references() -> None:
    inventory = build_inventory(ROOT)
    serialized = json.dumps(inventory)

    assert re.search(r"(?i)(?:phase|step)\d+", serialized) is None
