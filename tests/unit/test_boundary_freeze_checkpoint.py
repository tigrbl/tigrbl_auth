from __future__ import annotations

from pathlib import Path

import yaml

from tigrbl_auth.cli.boundary import validate_scope_freeze_metadata

ROOT = Path(__file__).resolve().parents[2]


def test_boundary_freeze_metadata_matches_retained_scope() -> None:
    scope = yaml.safe_load((ROOT / "compliance/targets/certification_scope.yaml").read_text(encoding="utf-8"))
    failures, summary = validate_scope_freeze_metadata(scope)
    assert failures == []
    assert summary["scope_freeze_present"] is True
    assert summary["scope_freeze_retained_target_count"] == 48
    assert summary["scope_freeze_retained_rfc_target_count"] == 30
    assert summary["scope_freeze_retained_non_rfc_target_count"] == 18
    assert summary["scope_freeze_deferred_target_count"] == 25
    assert summary["scope_freeze_retained_target_identity_hash_matches"] is True


def test_boundary_freeze_lists_required_prohibited_expansions() -> None:
    scope = yaml.safe_load((ROOT / "compliance/targets/certification_scope.yaml").read_text(encoding="utf-8"))
    freeze = scope["boundary_freeze"]
    prohibited = set(freeze["prohibited_expansions"])
    assert {
        "RFC 7800",
        "RFC 7952",
        "RFC 8291",
        "RFC 8812",
        "RFC 8932",
        "OAuth 2.1 alignment profile",
        "SAML IdP/SP",
        "LDAP/AD federation",
        "SCIM",
        "policy-platform/federation breadth outside the declared boundary",
    } <= prohibited
    assert freeze["no_target_count_drift_during_closeout"] is True
    assert freeze["closeout_scope_expansion_requires_separate_program"] is True
    assert freeze["fully_featured_claim_boundary_fixed"] is True
