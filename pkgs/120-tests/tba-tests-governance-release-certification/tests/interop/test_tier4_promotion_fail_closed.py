from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[5]


def _load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_tier4_claims_require_preserved_bundles() -> None:
    claims = _load_yaml(ROOT / "compliance" / "claims" / "declared-target-claims.yaml")
    evidence_manifest = _load_yaml(ROOT / "compliance" / "evidence" / "manifest.yaml")
    preserved = list((evidence_manifest.get("state") or {}).get("preserved_tier4_bundles") or [])
    tier4_targets = [
        str(claim.get("target"))
        for claim in claims.get("claim_set", {}).get("claims", [])
        if int(claim.get("tier", 0)) >= 4
    ]
    if tier4_targets:
        assert preserved
    else:
        assert preserved == [] or isinstance(preserved, list)


def test_tier4_candidates_do_not_count_as_preserved_bundles() -> None:
    evidence_manifest = _load_yaml(ROOT / "compliance" / "evidence" / "manifest.yaml")
    state = evidence_manifest.get("state") or {}
    candidates = list(state.get("tier4_candidate_layouts") or [])
    preserved = list(state.get("preserved_tier4_bundles") or [])
    assert candidates
    assert all("candidates/" in item for item in candidates)
    assert all("bundles/" in item or item.startswith("dist/") for item in preserved)
