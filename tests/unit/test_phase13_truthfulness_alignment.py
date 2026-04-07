from __future__ import annotations

import json
from pathlib import Path

import yaml

from tigrbl_auth.cli.claims import REQUIRED_BUCKET_LABELS
from tigrbl_auth.cli.feature_surface import REQUIRED_TARGET_BUCKETS
from tigrbl_auth.cli.truth import verify_truth_chain
from tigrbl_auth.config import deployment
from tigrbl_auth.config.deployment import resolve_deployment
from tigrbl_auth.config.settings import Settings


ROOT = Path(__file__).resolve().parents[2]
PROFILE_ORDER = ("baseline", "production", "hardening")
RECONCILED_TARGETS = {
    "RFC 7516": {
        "claim_profile": "baseline",
        "scope_bucket": "baseline-certifiable-now",
        "active_profiles": {"baseline", "production", "hardening"},
        "routes": [],
    },
    "RFC 7592": {
        "claim_profile": "production",
        "scope_bucket": "production-completion-required",
        "active_profiles": {"production", "hardening"},
        "routes": ["/register/{client_id}"],
    },
    "RFC 9207": {
        "claim_profile": "production",
        "scope_bucket": "production-completion-required",
        "active_profiles": {"production", "hardening"},
        "routes": ["/authorize", "/.well-known/openid-configuration"],
    },
}


def _load_yaml(relative_path: str) -> dict:
    return yaml.safe_load((ROOT / relative_path).read_text(encoding="utf-8"))


def _declared_claims_by_target() -> dict[str, dict]:
    claims = _load_yaml("compliance/claims/declared-target-claims.yaml")["claim_set"]["claims"]
    return {str(item["target"]): item for item in claims}


def _rfc_targets_by_label() -> dict[str, dict]:
    targets = _load_yaml("compliance/targets/rfc-targets.yaml")["targets"]
    return {str(item["label"]): item for item in targets}


def _scope_targets_by_label() -> dict[str, dict]:
    targets = _load_yaml("compliance/targets/certification_scope.yaml")["targets"]
    return {str(item["label"]): item for item in targets}


def _first_non_peer_profile(profiles: list[str]) -> str:
    for profile in profiles:
        if profile != "peer-claim":
            return profile
    raise AssertionError("every retained target must have a non-peer claim profile")


def _earliest_active_profile(label: str) -> str | None:
    for profile in PROFILE_ORDER:
        deployment_model = resolve_deployment(None, profile=profile)
        if label in set(deployment_model.active_targets):
            return profile
    return None


def test_rfc9700_settings_default_matches_deployment_default() -> None:
    settings = Settings()
    assert settings.enable_rfc9700 is True
    assert deployment.DEFAULT_VALUES["enable_rfc9700"] is True

    hardening_from_settings = resolve_deployment(settings, profile="hardening")
    hardening_from_defaults = resolve_deployment(None, profile="hardening")

    assert "RFC 9700" in set(hardening_from_settings.active_targets)
    assert set(hardening_from_settings.active_targets) == set(hardening_from_defaults.active_targets)


def test_repository_state_release_gate_claim_matches_current_release_report() -> None:
    repository_state = _load_yaml("compliance/claims/repository-state.yaml")["repository_state"]
    release_gate_report = json.loads((ROOT / "docs" / "compliance" / "release_gate_report.json").read_text())
    final_release_report = json.loads((ROOT / "docs" / "compliance" / "final_release_gate_report.json").read_text())

    assert repository_state["release_gate_passed_at_phase_13"] is release_gate_report["passed"]
    assert release_gate_report["passed"] is True
    assert final_release_report["passed"] is True


def test_reconciled_target_profiles_match_deployment_activation_and_declared_claims() -> None:
    claims_by_target = _declared_claims_by_target()
    rfc_targets_by_label = _rfc_targets_by_label()

    for label, expected in RECONCILED_TARGETS.items():
        claim_profile = expected["claim_profile"]
        assert _earliest_active_profile(label) == claim_profile
        assert claims_by_target[label]["profile"] == claim_profile
        assert _first_non_peer_profile(rfc_targets_by_label[label]["profiles"]) == claim_profile

        for profile in PROFILE_ORDER:
            active_targets = set(resolve_deployment(None, profile=profile).active_targets)
            if profile in expected["active_profiles"]:
                assert label in active_targets
            else:
                assert label not in active_targets


def test_reconciled_targets_have_no_scope_discrepancies_and_expected_buckets() -> None:
    scope = _load_yaml("compliance/targets/certification_scope.yaml")
    scope_by_label = _scope_targets_by_label()

    assert scope.get("discrepancy_summary", {}) == {}

    for label, expected in RECONCILED_TARGETS.items():
        entry = scope_by_label[label]
        assert entry["scope_bucket"] == expected["scope_bucket"]
        assert entry["first_claimable_profile"] == expected["claim_profile"]
        assert entry.get("discrepancies", []) == []


def test_bucket_constants_and_surface_truth_match_reconciled_targets() -> None:
    target_buckets = _load_yaml("compliance/targets/target-buckets.yaml")["buckets"]
    surface_truth = _load_yaml("compliance/targets/public-operator-surface.yaml")["surfaces"]["public_auth_plane"]["target"]["target_profile_truth"]

    expected_bucket_membership = {
        "RFC 7516": "baseline",
        "RFC 7592": "production",
        "RFC 9207": "production",
    }
    for label, bucket_name in expected_bucket_membership.items():
        assert label in set(target_buckets[bucket_name]["labels"])
        assert label in REQUIRED_BUCKET_LABELS[bucket_name]
        assert label in REQUIRED_TARGET_BUCKETS[bucket_name]
        for other_bucket in {"baseline", "production", "hardening"} - {bucket_name}:
            assert label not in set(target_buckets[other_bucket]["labels"])

    assert surface_truth["RFC 7516"]["profiles"] == ["baseline", "production", "hardening"]
    assert surface_truth["RFC 7516"]["routes"] == []
    assert surface_truth["RFC 7592"]["routes"] == RECONCILED_TARGETS["RFC 7592"]["routes"]
    assert surface_truth["RFC 9207"]["routes"] == RECONCILED_TARGETS["RFC 9207"]["routes"]


def test_repository_state_marks_truth_reconciliation_complete_and_executor_evidence_checkpoint_installed() -> None:
    repository_state = _load_yaml("compliance/claims/repository-state.yaml")["repository_state"]

    assert repository_state["phase_13_target_profile_truth_reconciled_complete"] is True
    assert repository_state["phase_13_profile_scope_mismatch_set_empty"] is True
    assert repository_state["phase_13_clean_room_executor_matrix_declared_complete"] is True
    assert repository_state["phase_13_validated_manifest_identity_contract_installed"] is True
    assert repository_state["phase_13_validated_runtime_matrix_preservation_complete"] is True
    assert repository_state["phase_13_validated_test_lane_preservation_complete"] is True
    assert repository_state["phase_13_validated_migration_portability_preservation_complete"] is True
    assert repository_state["alignment_only_checkpoint_no_new_certification_evidence"] is False


def _load_json(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def test_generated_reports_reflect_reconciled_target_profile_truth() -> None:
    rfc_family_status = _load_json("docs/compliance/rfc_family_status_report.json")
    assert rfc_family_status["summary"]["rfc_targets_with_scope_discrepancies"] == 0

    final_matrix = _load_json("docs/compliance/final_target_decision_matrix.json")
    rows = {row["target"]: row for row in final_matrix["rows"]}
    assert rows["RFC 7516"]["profile"] == "baseline"
    assert rows["RFC 7516"]["scope_bucket"] == "baseline-certifiable-now"
    assert rows["RFC 7592"]["profile"] == "production"
    assert rows["RFC 7592"]["scope_bucket"] == "production-completion-required"
    assert rows["RFC 9207"]["profile"] == "production"
    assert rows["RFC 9207"]["scope_bucket"] == "production-completion-required"

    current_state_md = (ROOT / "CURRENT_STATE.md").read_text(encoding="utf-8")
    certification_status_md = (ROOT / "CERTIFICATION_STATUS.md").read_text(encoding="utf-8")
    assert "validated runtime matrix green: `True`" in current_state_md
    assert "profile-scope mismatch set empty: `True`" in current_state_md
    assert "target_profile_truth_reconciled_complete: `True`" in certification_status_md
    assert "profile_scope_mismatch_set_empty: `True`" in certification_status_md


def test_truth_chain_verifier_passes_against_generated_artifacts() -> None:
    payload = verify_truth_chain(ROOT)
    assert payload["passed"] is True
