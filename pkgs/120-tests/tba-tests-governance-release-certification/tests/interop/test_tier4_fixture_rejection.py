from __future__ import annotations

from pathlib import Path

import yaml

from scripts.materialize_tier4_peer_evidence import _validate_external_artifacts, load_counterparts, load_peer_profiles
from scripts.stage_tier4_external_root_fixtures import stage


def test_repository_staged_fixtures_are_rejected_for_independent_claims(tmp_path: Path) -> None:
    fixture_root = tmp_path / "fixtures"
    stage(fixture_root)

    profile = load_peer_profiles()["browser"]
    counterpart = load_counterparts()["browser-rp"]
    manifest = yaml.safe_load((fixture_root / "browser" / "manifest.yaml").read_text(encoding="utf-8"))
    result = yaml.safe_load((fixture_root / "browser" / "result.yaml").read_text(encoding="utf-8"))

    failures = _validate_external_artifacts(
        fixture_root / "browser",
        "browser",
        profile,
        counterpart,
        manifest,
        result,
    )

    assert "non-independent evidence source" in failures
    assert "independence attestation class mismatch" in failures
    assert "peer operator is not independent" in failures
    assert "independence attestation missing package_team_member=false" in failures
    assert "independence attestation missing repository_fixture_generated=false" in failures
