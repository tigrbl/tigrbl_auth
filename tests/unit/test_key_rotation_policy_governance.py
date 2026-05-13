import pytest

from tigrbl_auth.services.key_rotation_policy import (
    EffectiveKeyRotationPolicy,
    KeyRotationAdministration,
    KeyRotationPolicyGovernance,
    KeyRotationPolicyOverlapError,
)


SCOPE = {
    "tenant_id": "tenant-a",
    "issuer": "https://issuer.example.test/tenant-a",
    "profile": "enterprise",
    "key_class": "asymmetric",
    "key_use": "sign",
    "algorithm": "EdDSA",
}


def _governance_with_published_policy() -> KeyRotationPolicyGovernance:
    governance = KeyRotationPolicyGovernance()
    governance.create_policy_version(
        "pol:jwt-signing",
        "v1",
        **SCOPE,
        cadence_days=30,
        max_key_age_days=45,
        overlap_seconds=300,
        retirement_seconds=600,
        emergency_triggers=("compromise", "operator-forced"),
        created_by="governance-owner",
        reason="baseline jwt signing rotation",
    )
    governance.approve_policy_version("pol:jwt-signing", "v1", actor="governance-approver")
    governance.publish_policy_version("pol:jwt-signing", "v1", actor="governance-publisher")
    return governance


@pytest.mark.unit
def test_governance_record_captures_rotation_scope_and_rules() -> None:
    governance = KeyRotationPolicyGovernance()

    policy = governance.create_policy_version(
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

    assert policy.status == "draft"
    assert policy.emergency_triggers == ("compromise", "operator-forced")
    assert policy.jwks_publish_required is True
    assert governance.versions[("pol:jwt-signing", "v1")] == policy


@pytest.mark.unit
def test_policy_version_lifecycle_approves_publishes_and_supersedes() -> None:
    governance = _governance_with_published_policy()
    governance.create_policy_version(
        "pol:jwt-signing",
        "v2",
        **SCOPE,
        cadence_days=15,
        max_key_age_days=30,
        overlap_seconds=300,
        retirement_seconds=600,
        emergency_triggers=("compromise",),
        created_by="governance-owner",
        reason="tighten jwt signing rotation",
    )
    governance.approve_policy_version("pol:jwt-signing", "v2", actor="governance-approver")

    published = governance.publish_policy_version("pol:jwt-signing", "v2", actor="governance-publisher")

    assert published.status == "published"
    assert published.supersedes == "v1"
    assert governance.versions[("pol:jwt-signing", "v1")].status == "retired"
    assert governance.require_effective_policy(**SCOPE).version_id == "v2"


@pytest.mark.unit
def test_effective_policy_projection_is_read_only_for_admin_runtime() -> None:
    governance = _governance_with_published_policy()

    effective = governance.require_effective_policy(**SCOPE)

    assert isinstance(effective, EffectiveKeyRotationPolicy)
    with pytest.raises(AttributeError):
        effective.cadence_days = 90  # type: ignore[misc]


@pytest.mark.unit
def test_fail_closed_without_effective_policy() -> None:
    admin = KeyRotationAdministration(KeyRotationPolicyGovernance())

    with pytest.raises(PermissionError, match="effective governance policy"):
        admin.execute_rotation(
            **SCOPE,
            actor="admin-operator",
            old_kid="old",
            new_kid="new",
            jwks_published=True,
            retired=True,
            reason="scheduled rotation",
        )


@pytest.mark.unit
def test_admin_policy_view_exposes_effective_policy_without_mutation() -> None:
    governance = _governance_with_published_policy()
    admin = KeyRotationAdministration(governance)

    effective = admin.view_effective_policy(**SCOPE)

    assert effective.policy_id == "pol:jwt-signing"
    assert not hasattr(admin, "create_policy_version")
    assert governance.versions[("pol:jwt-signing", "v1")].status == "published"


@pytest.mark.unit
def test_admin_policy_bound_execution_records_policy_version() -> None:
    governance = _governance_with_published_policy()
    admin = KeyRotationAdministration(governance, authorize=lambda request: "authz:decision-123")

    audit = admin.execute_rotation(
        **SCOPE,
        actor="admin-operator",
        old_kid="kid-old",
        new_kid="kid-new",
        jwks_published=True,
        retired=True,
        reason="scheduled rotation",
    )

    assert audit.policy_id == "pol:jwt-signing"
    assert audit.policy_version_id == "v1"
    assert audit.authorization_decision_ref == "authz:decision-123"


@pytest.mark.unit
def test_rotation_audit_evidence_contains_required_fields() -> None:
    governance = _governance_with_published_policy()
    admin = KeyRotationAdministration(governance)

    audit = admin.execute_rotation(
        **SCOPE,
        actor="admin-operator",
        old_kid="kid-old",
        new_kid="kid-new",
        jwks_published=True,
        retired=True,
        reason="scheduled rotation",
    )

    assert audit.audit_id == "kra:pol:jwt-signing:v1:kid-new"
    assert audit.actor == "admin-operator"
    assert audit.jwks_published is True
    assert audit.retired is True
    assert admin.audit_records == (audit,)


@pytest.mark.unit
def test_cross_plane_nonoverlap_guard_rejects_admin_policy_storage() -> None:
    governance = _governance_with_published_policy()
    admin = KeyRotationAdministration(governance)
    governance.assert_administration_does_not_own_policy(admin)

    class OverlappingAdministration:
        policy_store = {}

    with pytest.raises(KeyRotationPolicyOverlapError, match="governance policy authority"):
        governance.assert_administration_does_not_own_policy(OverlappingAdministration())
