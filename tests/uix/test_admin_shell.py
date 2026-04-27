from tigrbl_auth.uix import (
    ADMIN_NAVIGATION,
    AdminConsoleShell,
    AdminPrincipal,
    AdminSession,
    TenantProfileSelection,
)


def _admin_session() -> AdminSession:
    return AdminSession(
        session_id="sess-admin",
        authenticated=True,
        principal=AdminPrincipal(subject="admin@example.com", roles=("admin",)),
    )


def test_admin_shell_renders_authenticated_enterprise_navigation():
    shell = AdminConsoleShell(issuer="https://issuer.example", environment_label="local")
    state = shell.render(
        session=_admin_session(),
        selection=TenantProfileSelection(
            tenant_id="tenant-a",
            deployment_profile="baseline",
            surface_sets=("admin-rpc", "diagnostics"),
        ),
        readiness={
            "admin_authorized": True,
            "readiness_healthy": True,
            "contracts_valid": True,
            "migrations_current": True,
            "cookies_secure": True,
            "openrpc_available": True,
        },
    )

    assert state.principal_subject == "admin@example.com"
    assert state.navigation == ADMIN_NAVIGATION
    assert {"dashboard", "tenants", "keys-jwks", "policy-simulation"} <= set(state.navigation)
    assert state.warnings == ()


def test_admin_shell_exposes_tenant_profile_selector_and_environment_banner():
    shell = AdminConsoleShell(issuer="https://issuer.example", environment_label="dev")
    state = shell.render(
        session=_admin_session(),
        selection=TenantProfileSelection(
            tenant_id="tenant-b",
            deployment_profile="hardening",
            surface_sets=("admin-rpc",),
        ),
        readiness={
            "admin_authorized": True,
            "readiness_healthy": True,
            "contracts_valid": True,
            "migrations_current": True,
            "cookies_secure": True,
            "openrpc_available": True,
        },
    )

    payload = state.to_dict()
    assert payload["tenant_id"] == "tenant-b"
    assert payload["deployment_profile"] == "hardening"
    assert payload["issuer"] == "https://issuer.example"
    assert payload["environment_label"] == "dev"
    assert payload["active_surface_sets"] == ["admin-rpc"]
