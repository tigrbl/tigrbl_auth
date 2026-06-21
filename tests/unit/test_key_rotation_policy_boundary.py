import pytest

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for src in (ROOT / "pkgs").glob("*/src"):
    value = str(src)
    if value not in sys.path:
        sys.path.insert(0, value)

import tigrbl_identity_jose as jose
from tigrbl_identity_contracts.evidence.key_rotation import KeyRotationAuditEvidence


SCOPE = {
    "tenant_id": "tenant-a",
    "issuer": "https://issuer.example.test/tenant-a",
    "profile": "enterprise",
    "key_class": "asymmetric",
    "key_use": "sign",
    "algorithm": "EdDSA",
}


def _published_governance() -> jose.KeyRotationPolicyGovernance:
    governance = jose.KeyRotationPolicyGovernance()
    governance.create_policy_version(
        "pol:jwt-signing",
        "v1",
        **SCOPE,
        cadence_days=30,
        max_key_age_days=45,
        overlap_seconds=300,
        retirement_seconds=600,
        emergency_triggers=("operator-forced", "compromise", "compromise"),
        created_by="governance-owner",
        reason="baseline jwt signing rotation",
    )
    governance.approve_policy_version(
        "pol:jwt-signing",
        "v1",
        actor="governance-approver",
    )
    governance.publish_policy_version(
        "pol:jwt-signing",
        "v1",
        actor="governance-publisher",
    )
    return governance


def test_key_rotation_policy_boundary_t0_inventory_exports_policy_runtime_objects():
    assert jose.KeyRotationPolicyVersion.__name__ == "KeyRotationPolicyVersion"
    assert jose.EffectiveKeyRotationPolicy.__name__ == "EffectiveKeyRotationPolicy"
    assert not hasattr(jose, "KeyRotationAuditEvidence")
    assert KeyRotationAuditEvidence.__name__ == "KeyRotationAuditEvidence"
    assert jose.KeyRotationPolicyGovernance.__name__ == "KeyRotationPolicyGovernance"
    assert jose.KeyRotationAdministration.__name__ == "KeyRotationAdministration"
    assert jose.KeyRotationPolicyOverlapError.__name__ == "KeyRotationPolicyOverlapError"


def test_key_rotation_policy_boundary_t1_happy_path_publishes_and_executes_policy_bound_rotation():
    governance = _published_governance()
    admin = jose.KeyRotationAdministration(
        governance,
        authorize=lambda request: (
            f"authz:{request['policy_id']}:{request['policy_version_id']}"
        ),
    )

    effective = admin.view_effective_policy(**SCOPE)
    audit = admin.execute_rotation(
        **SCOPE,
        actor="admin-operator",
        old_kid="kid-old",
        new_kid="kid-new",
        jwks_published=True,
        retired=True,
        reason="scheduled rotation",
    )

    assert effective.policy_id == "pol:jwt-signing"
    assert effective.version_id == "v1"
    assert effective.emergency_triggers == ("compromise", "operator-forced")
    assert audit.policy_id == effective.policy_id
    assert audit.policy_version_id == effective.version_id
    assert audit.authorization_decision_ref == "authz:pol:jwt-signing:v1"
    assert audit.jwks_published is True
    assert audit.retired is True
    assert admin.audit_records == (audit,)


def test_key_rotation_policy_boundary_t2_fail_closed_guards_policy_publication_and_plane_overlap():
    governance = jose.KeyRotationPolicyGovernance()
    admin = jose.KeyRotationAdministration(governance, authorize=lambda _request: "")

    with pytest.raises(PermissionError, match="effective governance policy"):
        admin.execute_rotation(
            **SCOPE,
            actor="admin-operator",
            old_kid="kid-old",
            new_kid="kid-new",
            jwks_published=True,
            retired=True,
            reason="scheduled rotation",
        )

    governance = _published_governance()
    admin = jose.KeyRotationAdministration(governance)
    with pytest.raises(PermissionError, match="JWKS publication"):
        admin.execute_rotation(
            **SCOPE,
            actor="admin-operator",
            old_kid="kid-old",
            new_kid="kid-new",
            jwks_published=False,
            retired=True,
            reason="scheduled rotation",
        )
    with pytest.raises(PermissionError, match="old key retirement"):
        admin.execute_rotation(
            **SCOPE,
            actor="admin-operator",
            old_kid="kid-old",
            new_kid="kid-new",
            jwks_published=True,
            retired=False,
            reason="scheduled rotation",
        )

    class OverlappingAdministration:
        policy_store = {}

    with pytest.raises(jose.KeyRotationPolicyOverlapError):
        governance.assert_administration_does_not_own_policy(OverlappingAdministration())
