from datetime import datetime, timedelta, timezone

from tigrbl_authorization_contracts import (
    ActionDefinition,
    AuthorizationEffect,
    AuthorizationRequest,
    AuthenticationContext,
    PrincipalRef,
    ResourceRef,
    RoleDefinition,
    RoleGrant,
)
from tigrbl_authz_policy_decision_engine import PlatformPolicyDecisionEngine


def _engine(*, expires_at=None, required_acr=None, effect="allow"):
    return PlatformPolicyDecisionEngine(
        actions=[ActionDefinition("bucket.read", "bucket", required_acr=required_acr)],
        roles=[RoleDefinition("reader", "Reader", "tenant-a", actions=("bucket.read",))],
        grants=[
            RoleGrant(
                "grant-1",
                "tenant-a",
                PrincipalRef("alice", "user", tenant_id="tenant-a"),
                "reader",
                ResourceRef("bucket", "bucket-1", "tenant-a"),
                expires_at=expires_at,
                effect=effect,
            )
        ],
        policy_version="publication-1",
    )


def _request(tenant="tenant-a", *, acr=None):
    return AuthorizationRequest(
        principal=PrincipalRef("alice", "user", tenant_id="tenant-a"),
        action="bucket.read",
        resource=ResourceRef("bucket", "bucket-1", tenant),
        authentication=AuthenticationContext(acr=acr),
        correlation_id="corr-1",
    )


def test_matching_scoped_grant_allows_and_records_lineage() -> None:
    decision = _engine().evaluate(_request())
    assert decision.effect is AuthorizationEffect.ALLOW
    assert decision.matched_grant_ids == ("grant-1",)
    assert decision.matched_policy_versions == ("publication-1",)


def test_cross_tenant_expired_unknown_and_explicit_deny_fail_closed() -> None:
    assert _engine().evaluate(_request("tenant-b")).reason_code == "cross_tenant"
    expired = datetime.now(timezone.utc) - timedelta(seconds=1)
    assert _engine(expires_at=expired).evaluate(_request()).reason_code == "grant_expired"
    unknown = _request()
    object.__setattr__(unknown, "action", "bucket.delete")
    assert _engine().evaluate(unknown).reason_code == "unknown_action"
    assert _engine(effect="deny").evaluate(_request()).reason_code == "explicit_deny"


def test_assurance_obligation_requires_step_up() -> None:
    decision = _engine(required_acr="urn:tigrbl:aal2").evaluate(_request(acr="urn:tigrbl:aal1"))
    assert decision.effect is AuthorizationEffect.DENY
    assert decision.reason_code == "assurance_insufficient"
    assert decision.obligations == ("step_up",)


def test_explicit_deny_precedes_allow_and_missing_abac_facts_fail_closed() -> None:
    allow = _engine()._grants[0]
    deny = RoleGrant("grant-deny", "tenant-a", allow.principal, "reader", allow.resource, effect="deny")
    engine = PlatformPolicyDecisionEngine(actions=[ActionDefinition("bucket.read", "bucket")], roles=[RoleDefinition("reader", "Reader", "tenant-a", actions=("bucket.read",))], grants=[allow, deny], policy_version="publication-2")
    assert engine.evaluate(_request()).reason_code == "explicit_deny"
    conditional = RoleGrant("grant-conditional", "tenant-a", allow.principal, "reader", allow.resource, conditions={"risk": "low"})
    missing = PlatformPolicyDecisionEngine(actions=[ActionDefinition("bucket.read", "bucket")], roles=[RoleDefinition("reader", "Reader", "tenant-a", actions=("bucket.read",))], grants=[conditional], policy_version="publication-3").evaluate(_request())
    assert not missing.allowed
    assert missing.missing_facts == ("risk",)
