from __future__ import annotations

import pytest

from tigrbl_authz_policy.control_plane import (
    ADMIN_CLIENT_FIELDS,
    PUBLIC_CLIENT_FIELDS,
    ABACAdministrator,
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
from tigrbl_authz_policy_service_identity_registry import (
    ServiceIdentityRegistry as CanonicalServiceIdentityRegistry,
)


def _client() -> dict[str, object]:
    return {
        "id": "client-row-1",
        "tenant_id": "tenant-a",
        "name": "Portal",
        "client_id": "portal",
        "client_secret": "secret",
        "redirect_uris": ["https://app.example/callback"],
        "type": "confidential",
        "created_at": "2026-05-23T00:00:00Z",
        "enabled": True,
        "policy_tags": ["admin"],
    }


async def _policy_stack(administrator_storage) -> tuple[ServiceIdentityRegistry, RBACAdministrator, ABACAdministrator, DelegatedAdministrator, PolicyEngine]:
    services = ServiceIdentityRegistry()
    services.register_service(
        "svc:billing",
        tenant_id="tenant-a",
        name="Billing Worker",
        scopes=("invoice.read", "client.read"),
    )
    services.issue_credential("svc:billing", label="primary", raw_key="svc-secret")

    rbac = RBACAdministrator(administrator_storage)
    await rbac.upsert_role("tenant-admin", ("client.*", "tenant.read", "invoice.read"), tenant_id="tenant-a")
    await rbac.assign_role("user:admin", "tenant-admin", tenant_id="tenant-a")

    abac = ABACAdministrator(administrator_storage)
    await abac.upsert_policy(
        "same-tenant-mfa",
        permission="client.update",
        tenant_id="tenant-a",
        required_attributes={"tenant_id": "tenant-a", "mfa": True},
        dynamic_conditions=(DynamicCondition("risk_score", "lte", 20),),
    )
    await abac.upsert_policy(
        "service-same-tenant",
        permission="invoice.read",
        tenant_id="tenant-a",
        required_attributes={"tenant_id": "tenant-a", "service": True},
    )

    delegated = DelegatedAdministrator(administrator_storage)
    await delegated.grant_scope(
        "user:delegate",
        tenant_ids=("tenant-a",),
        permissions=("client.update", "tenant.read"),
        mutable_client_fields=("name", "enabled"),
    )
    return services, rbac, abac, delegated, PolicyEngine(rbac=rbac, abac=abac, delegated_admin=delegated)


def test_admin_policy_boundary_t0_runtime_client_field_exposure_is_guarded():
    assert ServiceIdentityRegistry is CanonicalServiceIdentityRegistry
    assert "client_secret" not in PUBLIC_CLIENT_FIELDS
    assert set(PUBLIC_CLIENT_FIELDS) < set(ADMIN_CLIENT_FIELDS)


@pytest.mark.asyncio
async def test_admin_policy_boundary_t1_composes_rbac_abac_delegation_service_identity_and_reports(administrator_storage):
    services, rbac, abac, delegated, engine = await _policy_stack(administrator_storage)
    service_auth = services.authenticate(
        "svc-secret",
        tenant_id="tenant-a",
        required_permission="invoice.read",
    )

    user_decision = await engine.evaluate(
        subject="user:admin",
        tenant_id="tenant-a",
        permission="client.update",
        attributes={"tenant_id": "tenant-a", "mfa": True, "risk_score": 10},
        patch_fields=("name",),
    )
    service_decision = await engine.evaluate(
        subject="svc:billing",
        tenant_id="tenant-a",
        permission="invoice.read",
        attributes={"tenant_id": "tenant-a", "service": True},
        actor_type="service",
        service_auth=service_auth,
    )
    simulation = await simulate_policy(
        rbac=rbac,
        abac=abac,
        subject="user:admin",
        permission="client.update",
        attributes={"tenant_id": "tenant-a", "mfa": True, "risk_score": 5},
        tenant_id="tenant-a",
    )
    visible_tenants = await filter_visible_tenants(
        [{"id": "tenant-a"}, {"id": "tenant-b"}],
        subject="user:delegate",
        delegated_admin=delegated,
    )
    report = await build_compliance_report(
        service_registry=services,
        rbac=rbac,
        abac=abac,
        delegated_admin=delegated,
        audit_events=engine.audit_events,
        tenant_ids=("tenant-a", "tenant-b"),
        clients=(_client(),),
    )

    assert user_decision.allowed
    assert service_decision.allowed
    assert simulation.allowed
    assert await rbac.effective_permissions("user:admin", "tenant-a") == ("client.*", "invoice.read", "tenant.read")
    assert visible_tenants == [{"id": "tenant-a"}]
    assert report["service_identities"]["active_service_count"] == 1
    assert report["policy_engine"]["audit_event_count"] == 2
    assert report["tenant_isolation"]["enforced"] is True


@pytest.mark.asyncio
async def test_admin_policy_boundary_t2_fails_closed_for_scope_drift_and_exposure_leaks(administrator_storage):
    services, _rbac, _abac, delegated, engine = await _policy_stack(administrator_storage)
    client = _client()

    public_view = await expose_client_record(client, plane="public")
    delegate_view = await expose_client_record(
        client,
        plane="admin",
        subject="user:delegate",
        delegated_admin=delegated,
    )
    denied_tenant = await engine.evaluate(
        subject="user:delegate",
        tenant_id="tenant-b",
        permission="client.update",
        attributes={"tenant_id": "tenant-b", "mfa": True, "risk_score": 0},
        patch_fields=("name",),
    )
    denied_attributes = await engine.evaluate(
        subject="user:admin",
        tenant_id="tenant-a",
        permission="client.update",
        attributes={"tenant_id": "tenant-a", "mfa": False, "risk_score": 0},
        patch_fields=("name",),
    )

    assert "client_secret" not in public_view
    assert "client_secret" not in delegate_view
    assert denied_tenant.allowed is False
    assert denied_tenant.reason == "permission denied by delegated tenant scope"
    assert denied_attributes.allowed is False
    assert denied_attributes.reason == "permission denied by ABAC attributes"

    with pytest.raises(PermissionError, match="unknown service credential"):
        services.authenticate("wrong-secret", tenant_id="tenant-a")
    with pytest.raises(PermissionError, match="delegated client mutation scope"):
        await assert_client_mutation_authority(
            subject="user:delegate",
            tenant_id="tenant-a",
            patch={"client_secret": "new-secret"},
            delegated_admin=delegated,
        )
    with pytest.raises(PermissionError, match="tenant mutation"):
        await assert_client_mutation_authority(
            subject="user:admin",
            tenant_id="tenant-a",
            patch={"tenant_id": "tenant-b"},
        )
