from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / ".ssot" / "registry.json"

T0_FEATURE_EXPECTATIONS = {
    "feat:tracked-openid-federation-target": {
        "title": "Tracked OpenID Federation target",
        "spec_ids": {"spc:1068"},
        "test_id": "tst:tracked-openid-federation-target.t0-contract",
    },
    "feat:tracked-spiffe-spire-target": {
        "title": "Tracked SPIFFE/SPIRE target",
        "spec_ids": {"spc:1066", "spc:1068"},
        "test_id": "tst:tracked-spiffe-spire-target.t0-contract",
    },
}


def _registry() -> dict:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def _rows_by_id(rows: list[dict]) -> dict[str, dict]:
    return {str(row["id"]): row for row in rows}


def test_t0_tracked_openid_federation_target_contract() -> None:
    registry = _registry()
    features = _rows_by_id(registry["features"])
    tests = _rows_by_id(registry["tests"])
    expected = T0_FEATURE_EXPECTATIONS["feat:tracked-openid-federation-target"]
    feature = features["feat:tracked-openid-federation-target"]
    test = tests[expected["test_id"]]

    assert feature["title"] == expected["title"]
    assert feature["implementation_status"] == "absent"
    assert feature["plan"]["horizon"] == "future"
    assert feature["plan"]["target_claim_tier"] == "T0"
    assert set(feature["spec_ids"]) == expected["spec_ids"]
    assert expected["test_id"] in feature["test_ids"]
    assert "execution" in test and isinstance(test["execution"], dict)
    assert test["execution"]["selector"] == "test_t0_tracked_openid_federation_target_contract"
    assert test["execution"]["expected"]["feature_id"] == feature["id"]


def test_t0_tracked_spiffe_spire_target_contract() -> None:
    registry = _registry()
    features = _rows_by_id(registry["features"])
    tests = _rows_by_id(registry["tests"])
    expected = T0_FEATURE_EXPECTATIONS["feat:tracked-spiffe-spire-target"]
    feature = features["feat:tracked-spiffe-spire-target"]
    test = tests[expected["test_id"]]

    assert feature["title"] == expected["title"]
    assert feature["implementation_status"] == "absent"
    assert feature["plan"]["horizon"] == "future"
    assert feature["plan"]["target_claim_tier"] == "T0"
    assert set(feature["spec_ids"]) == expected["spec_ids"]
    assert expected["test_id"] in feature["test_ids"]
    assert "execution" in test and isinstance(test["execution"], dict)
    assert test["execution"]["selector"] == "test_t0_tracked_spiffe_spire_target_contract"
    assert test["execution"]["expected"]["feature_id"] == feature["id"]
