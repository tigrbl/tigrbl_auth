from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_peer_matrix_report_tracks_missing_external_bundles_truthfully() -> None:
    payload = json.loads((ROOT / "docs" / "compliance" / "peer_matrix_report.json").read_text(encoding="utf-8"))
    summary = payload["summary"]
    assert summary["supported_peer_profile_count"] == 16
    assert summary["required_external_bundle_count"] == summary["supported_peer_profile_count"]
    assert summary["external_bundle_count"] == 16
    assert summary["valid_external_bundle_count"] == 0
    assert summary["invalid_external_bundle_count"] == summary["external_bundle_count"]
    assert summary["missing_external_bundle_count"] == len(summary["profiles_missing_external_bundles"])
    assert summary["strict_independent_claims_ready"] is False
