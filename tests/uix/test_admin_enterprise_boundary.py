import pytest

from tigrbl_policy_administration_memory_provider import (
    ABACAdministrator,
    RBACAdministrator,
    simulate_policy,
)

from tigrbl_auth.uix import (
    ADMIN_NAVIGATION,
    RESOURCE_VIEW_OPERATIONS,
    SAFE_MUTATION_METHODS,
    AdminAuthorizationError,
    AdminConsoleShell,
    AdminPrincipal,
    AdminSession,
    SafeMutationRequest,
    TenantProfileSelection,
    build_readiness_dashboard,
    build_resource_views,
    execute_safe_mutation,
)


def _admin_session() -> AdminSession:
    return AdminSession(
        session_id="sess-admin",
        authenticated=True,
        principal=AdminPrincipal(subject="admin@example.test", roles=("admin",)),
    )


def _healthy_readiness() -> dict[str, bool]:
    return {
        "admin_authorized": True,
        "readiness_healthy": True,
        "contracts_valid": True,
        "migrations_current": True,
        "cookies_secure": True,
        "openrpc_available": True,
    }


def test_admin_enterprise_boundary_t0_inventory_exposes_all_required_surfaces():
    assert {
        "dashboard",
        "tenants",
        "clients",
        "identities",
        "sessions",
        "tokens",
        "consents",
        "audit",
        "keys-jwks",
        "tenant-jwks",
        "profile-certification",
        "rbac",
        "abac",
        "policy-simulation",
    } <= set(ADMIN_NAVIGATION)
    assert set(RESOURCE_VIEW_OPERATIONS) == {
        "tenants",
        "clients",
        "identities",
        "sessions",
        "tokens",
        "consents",
        "audit",
        "keys-jwks",
        "profile-certification",
    }
    assert set(SAFE_MUTATION_METHODS) == {
        "revoke-session",
        "revoke-token",
        "revoke-consent",
        "lock-identity",
        "toggle-tenant",
        "toggle-client",
        "rotate-key",
        "publish-jwks",
        "update-client-registration",
    }


@pytest.mark.asyncio
async def test_admin_enterprise_boundary_t1_happy_path_composes_shell_views_mutations_and_policy(administrator_storage):
    shell = AdminConsoleShell(
        issuer="https://issuer.example.test",
        environment_label="test",
    )
    state = shell.render(
        session=_admin_session(),
        selection=TenantProfileSelection(
            tenant_id="tenant-a",
            deployment_profile="enterprise",
            surface_sets=("admin-rpc", "operator-uix"),
        ),
        readiness=_healthy_readiness(),
        diagnostics={"issuer": "https://issuer.example.test", "client_secret": "hidden"},
    )

    all_methods = {
        method for required in RESOURCE_VIEW_OPERATIONS.values() for method in required
    }
    resource_views = build_resource_views(all_methods)
    mutation = execute_safe_mutation(
        SafeMutationRequest(
            action="publish-jwks",
            target_id="tenant-a",
            confirmed=True,
            confirmation_text="publish-jwks:tenant-a",
        )
    )

    rbac = RBACAdministrator(administrator_storage)
    await rbac.upsert_role("security-admin", ("jwks.show",), tenant_id="tenant-a")
    await rbac.assign_role("admin@example.test", "security-admin", tenant_id="tenant-a")
    abac = ABACAdministrator(administrator_storage)
    await abac.upsert_policy(
        "same-tenant",
        permission="jwks.show",
        required_attributes={"tenant_id": "tenant-a", "mfa": True},
    )
    decision = await simulate_policy(
        rbac=rbac,
        abac=abac,
        subject="admin@example.test",
        permission="jwks.show",
        attributes={"tenant_id": "tenant-a", "mfa": True},
    )

    assert state.principal_subject == "admin@example.test"
    assert state.active_surface_sets == ("admin-rpc", "operator-uix")
    assert state.diagnostics["client_secret"] == "[REDACTED]"
    assert all(view.backed for view in resource_views.values())
    assert mutation.status == "executed"
    assert mutation.audit_event["outcome"] == "executed"
    assert decision.allowed
    assert decision.matched == ("security-admin", "same-tenant")


@pytest.mark.asyncio
async def test_admin_enterprise_boundary_t2_fail_closed_guards_for_auth_readiness_mutation_and_policy(administrator_storage):
    shell = AdminConsoleShell(
        issuer="https://issuer.example.test",
        environment_label="test",
    )
    with pytest.raises(AdminAuthorizationError):
        shell.render(
            session=AdminSession(session_id="anon", principal=None, authenticated=False),
            selection=TenantProfileSelection(
                tenant_id="tenant-a",
                deployment_profile="enterprise",
            ),
            readiness=_healthy_readiness(),
        )

    blocked_dashboard = build_readiness_dashboard(
        {
            **_healthy_readiness(),
            "contracts_valid": False,
            "migrations_current": False,
        },
        diagnostics={"jwt_secret": "hidden"},
    )
    blocked_mutation = execute_safe_mutation(
        SafeMutationRequest(action="rotate-key", target_id="kid-1")
    )

    rbac = RBACAdministrator(administrator_storage)
    await rbac.upsert_role("security-admin", ("key.rotate",), tenant_id="tenant-a")
    await rbac.assign_role("admin@example.test", "security-admin", tenant_id="tenant-a")
    abac = ABACAdministrator(administrator_storage)
    await abac.upsert_policy(
        "same-tenant",
        permission="key.rotate",
        required_attributes={"tenant_id": "tenant-a", "mfa": True},
    )
    denied = await simulate_policy(
        rbac=rbac,
        abac=abac,
        subject="admin@example.test",
        permission="key.rotate",
        attributes={"tenant_id": "tenant-a", "mfa": False},
    )

    assert blocked_dashboard.status == "blocked"
    assert blocked_dashboard.sections["database"] == "blocked"
    assert blocked_dashboard.diagnostics["jwt_secret"] == "[REDACTED]"
    assert blocked_mutation.status == "confirmation_required"
    assert blocked_mutation.audit_event["outcome"] == "blocked"
    assert not denied.allowed
    assert denied.reason == "permission denied by ABAC attributes"
