from __future__ import annotations

from pathlib import Path

from tigrbl_auth.cli.metadata import build_cli_conformance_snapshot, build_cli_contract_manifest
from tigrbl_auth.cli.reports import build_feature_completeness_report, generate_state_reports


ROOT = Path(__file__).resolve().parents[2]


def test_cli_contract_exposes_release_verify_and_required_operator_verbs() -> None:
    contract = build_cli_contract_manifest()
    release = next(item for item in contract["commands"] if item["name"] == "release")
    spec = next(item for item in contract["commands"] if item["name"] == "spec")

    assert {verb["name"] for verb in release["verbs"]} >= {"bundle", "sign", "verify", "status", "recertify"}
    assert {verb["name"] for verb in spec["verbs"]} >= {"generate", "validate", "diff", "report"}

    snapshot = build_cli_conformance_snapshot()
    assert snapshot["summary"]["passed"] is True
    assert snapshot["summary"]["missing_required_verbs"] == {}


def test_feature_completeness_report_tracks_release_verify_and_current_state() -> None:
    payload = build_feature_completeness_report(ROOT, report_dir=ROOT / "docs" / "compliance")
    summary = payload["summary"]
    details = payload["details"]

    assert summary["capability_count"] >= 10
    assert summary["required_release_verify_verb_present"] is True
    assert "build_sign_verify_release_bundles" in details
    assert details["build_sign_verify_release_bundles"]["passed"] is True
    assert (ROOT / "docs" / "compliance" / "feature_completeness_report.json").exists()
    assert (ROOT / "docs" / "compliance" / "feature_completeness_report.md").exists()

    state = generate_state_reports(ROOT)
    current = state["current_state"]
    gaps = state["certification_state"]["open_gaps"]
    assert current["feature_release_verify_verb_present"] is True
    assert current["feature_completeness_capability_count"] >= 10
    assert current["feature_completeness_failed_capability_count"] >= 0
    assert any("operator-visible package capabilities" in gap for gap in gaps) or current["fully_featured_package_boundary_now"] is True
