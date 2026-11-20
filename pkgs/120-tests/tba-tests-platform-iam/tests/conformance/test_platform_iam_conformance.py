from datetime import datetime, timezone

from tba_contracts_authorization import (
    ActionDefinition,
    AuthorizationEffect,
    AuthorizationRequest,
    PrincipalRef,
    ResourceRef,
    RoleDefinition,
    RoleGrant,
)
from tba_provider_authorization_policy_decision_engine import PlatformPolicyDecisionEngine
from tba_router_authorization_administration import assert_tenant_scope
from tba_router_relying_party_session import SECURE_COOKIE, require_csrf
from tba_app_backend_relying_party import RPDeployment, validate_separation
import pytest


def test_decision_is_deterministic_and_publication_linked() -> None:
    engine = PlatformPolicyDecisionEngine(
        actions=[ActionDefinition("tenant.read", "tenant")],
        roles=[RoleDefinition("auditor", "Auditor", "tenant-a", actions=("tenant.read",))],
        grants=[RoleGrant("g1", "tenant-a", PrincipalRef("alice", "user", tenant_id="tenant-a"), "auditor", ResourceRef("tenant", "tenant-a", "tenant-a"))],
        policy_version="pub:sha256:abc",
        clock=lambda: datetime(2026, 1, 1, tzinfo=timezone.utc),
    )
    request = AuthorizationRequest(
        principal=PrincipalRef("alice", "user", tenant_id="tenant-a"),
        action="tenant.read",
        resource=ResourceRef("tenant", "tenant-a", "tenant-a"),
        correlation_id="corr-1",
    )
    first = engine.evaluate(request)
    second = engine.evaluate(request)
    assert first.effect is AuthorizationEffect.ALLOW
    assert first.reason_code == second.reason_code
    assert first.matched_grant_ids == second.matched_grant_ids
    assert first.matched_policy_versions == ("pub:sha256:abc",)


def test_missing_grant_is_not_applicable_and_enforcement_denies() -> None:
    engine = PlatformPolicyDecisionEngine(actions=[ActionDefinition("tenant.read", "tenant")])
    decision = engine.evaluate(
        AuthorizationRequest(
            principal=PrincipalRef("alice", "user", tenant_id="tenant-a"),
            action="tenant.read",
            resource=ResourceRef("tenant", "tenant-a", "tenant-a"),
        )
    )
    assert decision.effect is AuthorizationEffect.DENY
    assert not decision.allowed
    assert decision.reason_code == "no_matching_grant"


def test_customer_admin_csrf_cookie_and_rp_planes_fail_closed() -> None:
    with pytest.raises(PermissionError, match="cross-tenant"):
        assert_tenant_scope("tenant-a", "tenant-b")
    assert SECURE_COOKIE == {"httponly": True, "secure": True, "samesite": "lax"}
    with pytest.raises(PermissionError, match="CSRF"):
        require_csrf("/v1/rp/logout", "cookie-token", None)
    customer = RPDeployment("customer", "customer-api", "customer_session", ("https://customer.example/callback",))
    internal = RPDeployment("internal", "internal-api", "internal_session", ("https://internal.example/callback",), "urn:tigrbl:aal2")
    validate_separation(customer, internal)
    with pytest.raises(ValueError, match="isolated"):
        validate_separation(customer, RPDeployment("customer", "other", "other_cookie", ("https://other.example/callback",)))
