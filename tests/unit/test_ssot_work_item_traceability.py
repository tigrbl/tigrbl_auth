from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
FEATURE_ID = "feat:governance-work-item-traceability"
CLAIM_ID = "clm:governance-work-item-traceability"
TEST_ID = "tst:tests-unit-test-ssot-work-item-traceability-py"
ADR_ID = "adr:1029"
SPEC_ID = "spc:1050"


def _registry() -> dict:
    return json.loads((ROOT / ".ssot" / "registry.json").read_text(encoding="utf-8"))


def _rows_by_id(rows: list[dict]) -> dict[str, dict]:
    return {str(row["id"]): row for row in rows}


def test_work_item_traceability_artifacts_are_registered_and_linked() -> None:
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
    assert feature["plan"]["horizon"] == "current"

    assert FEATURE_ID in claim["feature_ids"]
    assert TEST_ID in claim["test_ids"]
    assert claim["kind"] == "governance"

    assert FEATURE_ID in test_row["feature_ids"]
    assert CLAIM_ID in test_row["claim_ids"]
    assert test_row["path"] == "tests/unit/test_ssot_work_item_traceability.py"

    assert adrs[ADR_ID]["slug"] == "github-work-items-are-mirrored-in-ssot"
    assert specs[SPEC_ID]["slug"] == "work-item-traceability-policy"

    adr_doc = yaml.safe_load((ROOT / ".ssot" / "adr" / "ADR-1029-github-work-items-are-mirrored-in-ssot.yaml").read_text(encoding="utf-8"))
    spec_doc = yaml.safe_load((ROOT / ".ssot" / "specs" / "SPEC-1050-work-item-traceability-policy.yaml").read_text(encoding="utf-8"))

    assert "release-impacting GitHub issues and pull requests" in adr_doc["body"]
    assert "Each release-impacting GitHub issue or pull request maps to an SSOT work item entry." in spec_doc["body"]
    assert registry["guard_policies"]["certification"]["forbid_open_release_blocking_issues"] is True
