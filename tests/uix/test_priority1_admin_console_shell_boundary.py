from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
OPERATOR_SRC = ROOT / "pkgs" / "tigrbl-identity-operator" / "src"
if str(OPERATOR_SRC) not in sys.path:
    sys.path.append(str(OPERATOR_SRC))

import tigrbl_identity_operator.uix as operator_uix  # noqa: E402

from tigrbl_auth.uix import (  # noqa: E402
    ADMIN_NAVIGATION,
    AdminAuthorizationError,
    AdminConsoleShell,
    AdminPrincipal,
    AdminSession,
    TenantProfileSelection,
    priority1_admin_console_shell_boundary_integrity,
    priority1_admin_console_shell_boundary_manifest,
)


BOUNDARY_FEATURE_IDS = {
    "feat:uix-admin-console-shell",
    "feat:uix-admin-auth-session",
    "feat:uix-tenant-profile-selector",
}


def _healthy_readiness() -> dict[str, bool]:
    return {
        "admin_authorized": True,
        "readiness_healthy": True,
        "contracts_valid": True,
        "migrations_current": True,
        "cookies_secure": True,
        "openrpc_available": True,
    }


def _admin_session() -> AdminSession:
    return AdminSession(
        session_id="sess-admin",
        authenticated=True,
        principal=AdminPrincipal(subject="admin@example.test", roles=("admin",)),
    )


def test_priority1_admin_console_shell_boundary_t0_inventory_tracks_all_features():
    manifest = priority1_admin_console_shell_boundary_manifest()
    integrity = priority1_admin_console_shell_boundary_integrity()
    operator_manifest = operator_uix.priority1_admin_console_shell_boundary_manifest()
    operator_integrity = operator_uix.priority1_admin_console_shell_boundary_integrity()

    assert set(manifest) == BOUNDARY_FEATURE_IDS
    assert manifest == operator_manifest
    assert integrity["passed"] is True
    assert operator_integrity["passed"] is True
    assert integrity["feature_count"] == 3
    assert {"dashboard", "tenants", "identities", "tenant-jwks"} <= set(ADMIN_NAVIGATION)


def test_priority1_admin_console_shell_boundary_t1_composes_shell_session_and_tenant_profile():
    shell = AdminConsoleShell(issuer="https://issuer.example.test", environment_label="test")
    initial_selection = TenantProfileSelection(
        tenant_id="tenant-a",
        deployment_profile="baseline",
        surface_sets=("admin-rpc", "diagnostics"),
    )
    next_selection = TenantProfileSelection(
        tenant_id="tenant-b",
        deployment_profile="hardening",
        surface_sets=("admin-rpc", "operator-uix"),
    )

    state = shell.render(
        session=_admin_session(),
        selection=initial_selection,
        readiness=_healthy_readiness(),
        diagnostics={"issuer": "https://issuer.example.test", "client_secret": "hidden"},
    )
    golden_path = shell.golden_path(
        session=_admin_session(),
        initial_selection=initial_selection,
        next_selection=next_selection,
    )

    assert state.principal_subject == "admin@example.test"
    assert state.tenant_id == "tenant-a"
    assert state.deployment_profile == "baseline"
    assert state.active_surface_sets == ("admin-rpc", "diagnostics")
    assert state.diagnostics["client_secret"] == "[REDACTED]"
    assert state.warnings == ()
    assert golden_path["events"][0]["event"] == "admin.session.accepted"
    assert golden_path["events"][2]["tenant_id"] == "tenant-b"
    assert golden_path["events"][2]["deployment_profile"] == "hardening"


def test_priority1_admin_console_shell_boundary_t2_fails_closed_for_admin_session_and_profiles():
    shell = AdminConsoleShell(issuer="https://issuer.example.test", environment_label="test")
    selection = TenantProfileSelection(tenant_id="tenant-a", deployment_profile="baseline")

    with pytest.raises(AdminAuthorizationError, match="authenticated admin session"):
        shell.render(
            session=AdminSession(session_id="sess-anon", authenticated=False, principal=None),
            selection=selection,
            readiness=_healthy_readiness(),
        )

    with pytest.raises(AdminAuthorizationError, match="administrator authorization"):
        shell.render(
            session=AdminSession(
                session_id="sess-user",
                authenticated=True,
                principal=AdminPrincipal(subject="user@example.test", roles=("support",)),
            ),
            selection=selection,
            readiness=_healthy_readiness(),
        )

    degraded = shell.render(
        session=AdminSession(
            session_id="sess-scope-admin",
            authenticated=True,
            principal=AdminPrincipal(subject="scoped@example.test", scopes=("tigrbl_auth:admin",)),
        ),
        selection=selection,
        readiness={**_healthy_readiness(), "contracts_valid": False, "cookies_secure": False},
        diagnostics={
            "jwt_secret": "hidden",
            "database": {"password": "db-secret", "host": "localhost"},
        },
    )

    assert {warning.code for warning in degraded.warnings} == {"contracts_valid", "cookies_secure"}
    assert degraded.diagnostics["jwt_secret"] == "[REDACTED]"
    assert degraded.diagnostics["database"]["password"] == "[REDACTED]"
    assert degraded.diagnostics["database"]["host"] == "localhost"
