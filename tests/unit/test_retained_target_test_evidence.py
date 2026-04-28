from __future__ import annotations

import re
from pathlib import Path

import yaml


def _load_yaml(path: Path) -> dict:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def _target_key(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.strip().lower()).strip("-")
    return f"target:{slug}"


def test_completed_retained_targets_have_classified_deterministic_tests() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    claim_payload = _load_yaml(repo_root / "compliance" / "claims" / "effective-target-claims.production.yaml")
    feature_to_test = _load_yaml(repo_root / "compliance" / "mappings" / "feature-to-test.yaml")
    classifications = _load_yaml(repo_root / "compliance" / "mappings" / "test_classification.yaml")

    categorized_tests = {
        path
        for paths in (classifications.get("categories") or {}).values()
        for path in (paths or [])
    }
    completed_claims = []
    for claim in ((claim_payload.get("claim_set") or {}).get("claims") or []):
        if str(claim.get("status") or "").strip() in {"planned", "deferred", "unsupported", "not-applicable"}:
            continue
        completed_claims.append(str(claim.get("target") or "").strip())

    missing_targets: list[str] = []
    missing_classified_tests: list[str] = []
    for target in sorted({item for item in completed_claims if item}):
        key = _target_key(target)
        mapped_tests = list(feature_to_test.get(key) or [])
        if not mapped_tests:
            missing_targets.append(target)
            continue
        if not all(test_path in categorized_tests for test_path in mapped_tests):
            missing_classified_tests.append(target)

    assert not missing_targets, f"Completed retained targets without test mappings: {missing_targets}"
    assert not missing_classified_tests, f"Completed retained targets without classified deterministic tests: {missing_classified_tests}"
