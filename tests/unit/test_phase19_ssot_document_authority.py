from __future__ import annotations

import json
from pathlib import Path

import yaml

from tigrbl_auth.document_authority import SSOT_DOCUMENT_AUTHORITY_SPEC


ROOT = Path(__file__).resolve().parents[2]
FEATURE_ID = "feat:governance-ssot-document-authority"
CLAIM_ID = "clm:governance-ssot-document-authority"
TEST_ID = "tst:tests-unit-test-phase19-ssot-document-authority-py"
ADR_ID = "adr:1031"
SPEC_ID = "spc:1052"


def _registry() -> dict:
    return json.loads((ROOT / ".ssot" / "registry.json").read_text(encoding="utf-8"))


def _rows_by_id(rows: list[dict]) -> dict[str, dict]:
    return {str(row["id"]): row for row in rows}


def test_ssot_document_authority_artifacts_are_registered_and_linked() -> None:
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
    assert test_row["path"] == "tests/unit/test_phase19_ssot_document_authority.py"

    assert adrs[ADR_ID]["slug"] == "ssot-is-the-authoritative-active-document"
    assert specs[SPEC_ID]["slug"] == "ssot-document-authority"

    adr_doc = yaml.safe_load(
        (ROOT / ".ssot" / "adr" / "ADR-1031-ssot-is-the-authoritative-active-document.yaml").read_text(
            encoding="utf-8"
        )
    )
    spec_doc = yaml.safe_load((ROOT / SSOT_DOCUMENT_AUTHORITY_SPEC).read_text(encoding="utf-8"))
    authority = spec_doc["document_authority"]

    assert "authoritative active document" in adr_doc["body"]
    assert "SSOT is the authoritative active document" in spec_doc["body"]
    assert authority["projection_manifest"] == "compliance/targets/document-authority.yaml"
    assert ".ssot/registry.json" in authority["canonical_ssot_roots"]
    assert "docs/compliance/truth_chain.md" in authority["authoritative_current_docs"]
