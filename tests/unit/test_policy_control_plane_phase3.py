import pytest

from tigrbl_auth.uix import (
    ABACAdministrator,
    ADMIN_CLIENT_FIELDS,
    PUBLIC_CLIENT_FIELDS,
    AttributePolicy,
    DelegatedAdministrator,
    DynamicCondition,
    PolicyEngine,
    RBACAdministrator,
    ServiceIdentityRegistry,
    assert_client_mutation_authority,
    build_compliance_report,
    expose_client_record,
    filter_visible_tenants,
    simulate_policy,
)
from tigrbl_authz_policy import (
    ABACAdministrator as CanonicalABACAdministrator,
    AttributePolicy as CanonicalAttributePolicy,
    DynamicCondition as CanonicalDynamicCondition,
)
from tigrbl_authz_policy import (
    DelegatedAdministrator as CanonicalDelegatedAdministrator,
)
from tigrbl_authz_policy import PolicyEngine as CanonicalPolicyEngine
from tigrbl_authz_policy import (
    ServiceIdentityRegistry as CanonicalServiceIdentityRegistry,
)
from tigrbl_authz_policy import (
    RBACAdministrator as CanonicalRBACAdministrator,
)


def test_service_identities_support_tenant_scoped_authentication_and_revocation():
    assert ServiceIdentityRegistry is CanonicalServiceIdentityRegistry
    registry = ServiceIdentityRegistry()
    service = registry.register_service(
        "svc-notifier",
        tenant_id="tenant-a",
        name="notifier",
        scopes=("client.read", "client.update"),
    )
    credential = registry.issue_credential(service.service_id, label="primary")

    auth = registry.authenticate(credential.raw_key, tenant_id="tenant-a", required_permission="client.read")

    assert auth.service.service_id == "svc-notifier"
    assert auth.granted_permissions == ("client.read", "client.update")

    registry.revoke_credential(credential.credential_id)

    try:
        registry.authenticate(credential.raw_key, tenant_id="tenant-a", required_permission="client.read")
    except PermissionError as exc:
        assert "revoked" in str(exc)
    else:  # pragma: no cover - fail closed if the registry stops revoking.
        raise AssertionError("revoked service credential unexpectedly authenticated")


def test_administrator_hard_rename_exports_only_new_names():
    import tigrbl_auth.uix as uix
    import tigrbl_authz_policy as authz_policy

    for module in (uix, authz_policy):
        assert module.RBACAdministrator is CanonicalRBACAdministrator
        assert module.ABACAdministrator is CanonicalABACAdministrator
        assert module.DelegatedAdministrator is CanonicalDelegatedAdministrator
        assert module.PolicyEngine is CanonicalPolicyEngine
        assert hasattr(module, "RBACAdministrator")
        assert hasattr(module, "ABACAdministrator")
        assert hasattr(module, "DelegatedAdministrator")
        assert not hasattr(module, "RBACAdministration")
        assert not hasattr(module, "ABACAdministration")
        assert not hasattr(module, "DelegatedAdministration")


@pytest.mark.asyncio
async def test_rbac_supports_inheritance_tenant_scoping_and_fine_grained_denies(administrator_storage):
    rbac = RBACAdministrator(administrator_storage)
    await rbac.upsert_role("support-reader", ("tenant.read", "client.read"), tenant_id="tenant-a")
    await rbac.upsert_role(
        "support-editor",
        ("client.update",),
        tenant_id="tenant-a",
        denied_permissions=("client.update.secret",),
        inherited_roles=("support-reader",),
    )
    await rbac.assign_role("alice", "support-editor", tenant_id="tenant-a")

    reader = RBACAdministrator(administrator_storage)
    allowed = await reader.decide("alice", "client.update", "tenant-a")
    denied = await reader.decide("alice", "client.update.secret", "tenant-a")
    wrong_tenant = await reader.decide("alice", "client.update", "tenant-b")

    assert allowed.allowed
    assert set(await reader.effective_permissions("alice", "tenant-a")) == {"client.read", "client.update", "tenant.read"}
    assert not denied.allowed
    assert "denied" in denied.reason
    assert not wrong_tenant.allowed


@pytest.mark.asyncio
async def test_policy_engine_supports_abac_dynamic_conditions_simulation_and_audit(administrator_storage):
    assert ABACAdministrator is CanonicalABACAdministrator
    assert AttributePolicy is CanonicalAttributePolicy
    assert DynamicCondition is CanonicalDynamicCondition
    assert PolicyEngine is CanonicalPolicyEngine

    rbac = RBACAdministrator(administrator_storage)
    await rbac.upsert_role("security-admin", ("key.rotate",), tenant_id="tenant-a")
    await rbac.assign_role("alice", "security-admin", tenant_id="tenant-a")

    abac = ABACAdministrator(administrator_storage)
    policy = await abac.upsert_policy(
        "same-tenant-mfa-risk",
        permission="key.rotate",
        required_attributes={"tenant_id": "tenant-a", "mfa": True},
        dynamic_conditions=(DynamicCondition(field="risk", operator="lte", expected=2),),
    )

    allowed = await simulate_policy(
        rbac=rbac,
        abac=abac,
        subject="alice",
        permission="key.rotate",
        attributes={"tenant_id": "tenant-a", "mfa": True, "risk": 1},
    )
    denied = await simulate_policy(
        rbac=rbac,
        abac=abac,
        subject="alice",
        permission="key.rotate",
        attributes={"tenant_id": "tenant-a", "mfa": True, "risk": 7},
    )

    engine = PolicyEngine(db=administrator_storage, rbac=rbac, abac=abac)
    engine_decision = await engine.evaluate(
        subject="alice",
        permission="key.rotate",
        tenant_id="tenant-a",
        attributes={"tenant_id": "tenant-a", "mfa": True, "risk": 1},
    )

    assert isinstance(policy, AttributePolicy)
    assert allowed.allowed
    assert not denied.allowed
    assert engine_decision.allowed
    assert len(engine.audit_events) == 1
    assert engine.audit_events[0].permission == "key.rotate"


@pytest.mark.asyncio
async def test_delegated_administrator_controls_tenant_visibility_and_client_exposure(administrator_storage):
    delegated = DelegatedAdministrator(administrator_storage)
    await delegated.grant_scope(
        "operator:tenant-a",
        tenant_ids=("tenant-a",),
        permissions=("client.read", "client.update"),
        visible_client_fields=("id", "tenant_id", "name", "client_id", "redirect_uris", "type"),
        mutable_client_fields=("name", "redirect_uris"),
    )
    tenants = [
        {"id": "tenant-a", "name": "Tenant A"},
        {"id": "tenant-b", "name": "Tenant B"},
    ]
    client = {
        "id": "client-1",
        "tenant_id": "tenant-a",
        "name": "Portal",
        "client_id": "client-portal",
        "client_secret": "secret-value",
        "redirect_uris": ["https://portal.example/callback"],
        "type": "confidential",
        "created_at": "2026-05-05T00:00:00+00:00",
    }

    reader = DelegatedAdministrator(administrator_storage)
    visible = await filter_visible_tenants(tenants, subject="operator:tenant-a", delegated_admin=reader)
    delegated_view = await expose_client_record(client, plane="admin", subject="operator:tenant-a", delegated_admin=reader)
    public_view = await expose_client_record(client, plane="public")

    assert [tenant["id"] for tenant in visible] == ["tenant-a"]
    assert set(delegated_view) == {"id", "tenant_id", "name", "client_id", "redirect_uris", "type"}
    assert delegated_view["name"] == "Portal"
    assert "client_secret" not in delegated_view
    assert tuple(public_view) == PUBLIC_CLIENT_FIELDS

    await assert_client_mutation_authority(
        subject="operator:tenant-a",
        tenant_id="tenant-a",
        patch={"name": "Portal 2"},
        delegated_admin=reader,
    )
    try:
        await assert_client_mutation_authority(
            subject="operator:tenant-a",
            tenant_id="tenant-a",
            patch={"client_secret": "rotated"},
            delegated_admin=reader,
        )
    except PermissionError as exc:
        assert "delegated client mutation scope" in str(exc)
    else:  # pragma: no cover - fail closed if delegated mutation checks regress.
        raise AssertionError("delegated mutation unexpectedly allowed a secret rotation")


@pytest.mark.asyncio
async def test_compliance_report_summarizes_cross_plane_policy_state(administrator_storage):
    registry = ServiceIdentityRegistry()
    registry.register_service(
        "svc-notifier",
        tenant_id="tenant-a",
        name="notifier",
        scopes=("client.read",),
    )
    rbac = RBACAdministrator(administrator_storage)
    await rbac.upsert_role("auditor", ("audit.read",), tenant_id="tenant-a")
    await rbac.assign_role("dana", "auditor", tenant_id="tenant-a")
    abac = ABACAdministrator(administrator_storage)
    await abac.upsert_policy(
        "tenant-a-audit",
        permission="audit.read",
        required_attributes={"tenant_id": "tenant-a"},
    )
    delegated = DelegatedAdministrator(administrator_storage)
    await delegated.grant_scope("delegate", tenant_ids=("tenant-a",), permissions=("client.read",))
    engine = PolicyEngine(rbac=rbac, abac=abac, delegated_admin=delegated)
    await engine.evaluate(
        subject="dana",
        permission="audit.read",
        tenant_id="tenant-a",
        attributes={"tenant_id": "tenant-a"},
    )

    report = await build_compliance_report(
        service_registry=registry,
        rbac=rbac,
        abac=abac,
        delegated_admin=delegated,
        audit_events=engine.audit_events,
        tenant_ids=("tenant-a", "tenant-b"),
        clients=(
            {
                "id": "client-1",
                "tenant_id": "tenant-a",
                "name": "Portal",
                "client_id": "client-portal",
                "client_secret": "hidden",
                "redirect_uris": ["https://portal.example/callback"],
                "type": "confidential",
                "created_at": "2026-05-05T00:00:00+00:00",
            },
        ),
    )

    assert report["tenant_isolation"]["enforced"]
    assert report["tenant_isolation"]["tenants"] == ["tenant-a", "tenant-b"]
    assert report["service_identities"]["active_service_count"] == 1
    assert report["policy_engine"]["role_count"] == 1
    assert report["policy_engine"]["policy_count"] == 1
    assert report["policy_engine"]["audit_event_count"] == 1
    assert report["client_exposure"]["admin_fields"] == list(ADMIN_CLIENT_FIELDS)
    assert report["recent_audit"][0]["subject"] == "dana"
