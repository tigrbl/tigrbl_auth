from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
FEATURE_ID = "feat:governance-dependency-compatibility-maintenance"
CLAIM_ID = "clm:governance-dependency-compatibility-maintenance"
TEST_ID = "tst:tests-unit-test-ssot-dependency-maintenance-traceability-py"
ADR_ID = "adr:1030"
SPEC_ID = "spc:1051"
PIN_TEST_ID = "tst:tests-unit-test-published-dependency-model-py"


def _registry() -> dict:
    return json.loads((ROOT / ".ssot" / "registry.json").read_text(encoding="utf-8"))


def _rows_by_id(rows: list[dict]) -> dict[str, dict]:
    return {str(row["id"]): row for row in rows}


def test_dependency_maintenance_artifacts_are_registered_and_linked() -> None:
    registry = _registry()
    features = _rows_by_id(registry["features"])
    claims = _rows_by_id(registry["claims"])
    tests = _rows_by_id(registry["tests"])
    adrs = _rows_by_id(registry["adrs"])
    specs = _rows_by_id(registry["specs"])

    feature = features[FEATURE_ID]
    claim = claims[CLAIM_ID]
    test_row = tests[TEST_ID]

    assert CLAIM_ID in feature["claim_ids"]
    assert TEST_ID in feature["test_ids"]
    assert PIN_TEST_ID in feature["test_ids"]

    assert FEATURE_ID in claim["feature_ids"]
    assert TEST_ID in claim["test_ids"]
    assert PIN_TEST_ID in claim["test_ids"]
    assert claim["tier"] == "T1"

    assert FEATURE_ID in test_row["feature_ids"]
    assert CLAIM_ID in test_row["claim_ids"]
    assert test_row["path"] == "tests/unit/test_ssot_dependency_maintenance_traceability.py"

    assert adrs[ADR_ID]["slug"] == "dependency-maintenance-is-governed-work"
    assert specs[SPEC_ID]["slug"] == "dependency-compatibility-maintenance"

    adr_doc = yaml.safe_load((ROOT / ".ssot" / "adr" / "ADR-1030-dependency-maintenance-is-governed-work.yaml").read_text(encoding="utf-8"))
    spec_doc = yaml.safe_load((ROOT / ".ssot" / "specs" / "SPEC-1051-dependency-compatibility-maintenance.yaml").read_text(encoding="utf-8"))

    assert "dependency upgrades that can change runtime behavior" in adr_doc["body"]
    assert "Dependency maintenance is a governed capability" in spec_doc["body"]

    pyproject_text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'pydantic[email]==2.12.5' in pyproject_text
    assert 'pytest-asyncio==1.3.0' in pyproject_text
