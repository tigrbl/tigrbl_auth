import pytest

from tigrbl_auth.uix import (
    AdminAuthorizationError,
    AdminConsoleShell,
    AdminPrincipal,
    AdminSession,
    TenantProfileSelection,
)


def _shell() -> AdminConsoleShell:
    return AdminConsoleShell(issuer="https://issuer.example", environment_label="local")


def _selection() -> TenantProfileSelection:
    return TenantProfileSelection(tenant_id="tenant-a", deployment_profile="baseline")


def _healthy() -> dict[str, bool]:
    return {
        "admin_authorized": True,
        "readiness_healthy": True,
        "contracts_valid": True,
        "migrations_current": True,
        "cookies_secure": True,
        "openrpc_available": True,
    }


def test_admin_shell_denies_unauthenticated_users():
    with pytest.raises(AdminAuthorizationError, match="authenticated admin session"):
        _shell().render(
            session=AdminSession(session_id="sess-anon", authenticated=False, principal=None),
            selection=_selection(),
            readiness=_healthy(),
        )


def test_admin_shell_denies_users_without_admin_authorization():
    with pytest.raises(AdminAuthorizationError, match="administrator authorization"):
        _shell().render(
            session=AdminSession(
                session_id="sess-user",
                authenticated=True,
                principal=AdminPrincipal(subject="user@example.com", roles=("support",)),
            ),
            selection=_selection(),
            readiness=_healthy(),
        )


def test_admin_shell_redacts_secret_configuration_values():
    state = _shell().render(
        session=AdminSession(
            session_id="sess-admin",
            authenticated=True,
            principal=AdminPrincipal(subject="admin@example.com", scopes=("tigrbl_auth:admin",)),
        ),
        selection=_selection(),
        readiness={
            "admin_authorized": True,
            "readiness_healthy": False,
            "contracts_valid": False,
            "migrations_current": True,
            "cookies_secure": False,
            "openrpc_available": True,
        },
        diagnostics={
            "jwt_secret": "plain-secret",
            "database": {"password": "db-secret", "host": "localhost"},
            "issuer": "https://issuer.example",
        },
    )

    assert state.diagnostics["jwt_secret"] == "[REDACTED]"
    assert state.diagnostics["database"]["password"] == "[REDACTED]"
    assert state.diagnostics["database"]["host"] == "localhost"
    assert {warning.code for warning in state.warnings} == {
        "readiness_healthy",
        "contracts_valid",
        "cookies_secure",
    }
