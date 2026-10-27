from datetime import datetime, timedelta, timezone

import pytest

from tigrbl_authorization_contracts import (
    ActionDefinition,
    AuthorizationDecision,
    AuthorizationEffect,
    AuthorizationRequest,
    AuthenticationContext,
    PrincipalRef,
    ResourceRef,
    RoleDefinition,
    RoleGrant,
)


def test_contracts_express_actor_resource_action_scope_and_assurance() -> None:
    principal = PrincipalRef("alice", "user", tenant_id="tenant-a")
    resource = ResourceRef("bucket", "bucket-1", "tenant-a", scope_path=("bucket-1",))
    request = AuthorizationRequest(
        principal=principal,
        action="bucket.read",
        resource=resource,
        authentication=AuthenticationContext(acr="urn:tigrbl:aal2", amr=("pwd", "otp")),
        correlation_id="corr-1",
    )
    assert request.principal.tenant_id == request.resource.tenant_id
    assert request.authentication.acr == "urn:tigrbl:aal2"


def test_role_grant_rejects_invalid_time_window() -> None:
    now = datetime.now(timezone.utc)
    with pytest.raises(ValueError, match="expires_at"):
        RoleGrant(
            grant_id="grant-1",
            tenant_id="tenant-a",
            principal=PrincipalRef("alice", "user", tenant_id="tenant-a"),
            role_id="role-1",
            resource=ResourceRef("tenant", "tenant-a", "tenant-a"),
            valid_from=now,
            expires_at=now - timedelta(seconds=1),
        )


def test_decision_contract_preserves_reason_lineage_and_obligations() -> None:
    decision = AuthorizationDecision(
        decision_id="decision-1",
        effect=AuthorizationEffect.DENY,
        reason_code="assurance_insufficient",
        matched_role_ids=("role-1",),
        matched_grant_ids=("grant-1",),
        matched_policy_versions=("policy-1:v2",),
        obligations=("step_up",),
    )
    assert not decision.allowed
    assert decision.obligations == ("step_up",)


def test_action_and_role_keys_are_normalized_and_nonempty() -> None:
    action = ActionDefinition("bucket.read", "bucket")
    role = RoleDefinition("role-reader", "Reader", "tenant-a", actions=(action.key,))
    assert role.actions == ("bucket.read",)
    with pytest.raises(ValueError):
        ActionDefinition("", "bucket")
