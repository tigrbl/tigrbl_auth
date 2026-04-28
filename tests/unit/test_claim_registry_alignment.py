from __future__ import annotations

from pathlib import Path

import yaml

from tigrbl_auth.cli.claim_registry import verify_claim_registries
from tigrbl_auth.config.deployment import resolve_deployment


ROOT = Path(__file__).resolve().parents[2]


def _load_yaml(relative_path: str) -> dict:
    return yaml.safe_load((ROOT / relative_path).read_text(encoding="utf-8"))


def test_claim_registry_verifier_passes() -> None:
    payload = verify_claim_registries(ROOT)
    assert payload["passed"] is True
    assert payload["core_targets_missing_from_feature_map"] == 0
    assert payload["extension_targets_missing_from_feature_map"] == 0
    assert payload["settings_backed_flags_missing_from_flag_map"] == 0


def test_fapi2_security_profile_is_declared_and_enforced() -> None:
    profiles = _load_yaml("compliance/targets/profiles.yaml")["profiles"]
    assert "fapi2-security" in profiles

    deployment = resolve_deployment(None, profile="fapi2-security")
    assert deployment.profile == "fapi2-security"
    assert deployment.flag_enabled("enable_rfc8705") is True
    assert deployment.flag_enabled("enable_rfc9101") is True
    assert deployment.flag_enabled("enable_rfc9126") is True
    assert deployment.flag_enabled("enable_rfc9396") is True


def test_claim_registry_imports_fapi_atomic_claims() -> None:
    claim_registry = _load_yaml("compliance/claims/claim-registry.yaml")
    claim_ids = {item["id"] for item in claim_registry["claims"]}
    assert "fapi2-security.par-required" in claim_ids
    assert "fapi2-security.jar-required" in claim_ids
    assert "fapi2-security.rar-required" in claim_ids
    assert "fapi2-security.issuer-identification" in claim_ids
    assert "fapi2-security.sender-constrained-tokens" in claim_ids
    assert "fapi2-security.security-bcp" in claim_ids


def test_repository_state_tracks_claim_model_completion() -> None:
    repository_state = _load_yaml("compliance/claims/repository-state.yaml")["repository_state"]
    assert repository_state["claim_registry_canonical_complete"] is True
    assert repository_state["fapi2_security_profile_declared_complete"] is True
    assert repository_state["release_claims_machine_derivable"] is True
    assert repository_state["core_targets_missing_from_feature_map"] == 0
    assert repository_state["extension_targets_missing_from_feature_map"] == 0
    assert repository_state["settings_backed_flags_missing_from_flag_map"] == 0
