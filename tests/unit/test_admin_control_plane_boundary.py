from __future__ import annotations

import ast
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
for src in (ROOT / "pkgs").glob("*/src"):
    value = str(src)
    if value not in sys.path:
        sys.path.insert(0, value)

from tigrbl_identity_admin import (  # noqa: E402
    AdminControlPlane,
    AdminControlPlaneError,
    AdminResourceKind,
    AdminResourceStatus,
    AdminUiState,
)


def _seed_control_plane() -> tuple[AdminControlPlane, str]:
    admin = AdminControlPlane()
    principal = admin.create_principal(
        actor="admin:root",
        tenant_id="tenant-a",
        subject="user:123",
        name="Tenant User",
        roles=("member",),
    )
    return admin, principal.id


@pytest.mark.unit
def test_admin_t0_public_surfaces_are_importable() -> None:
    admin, principal_id = _seed_control_plane()

    principal = admin.get(AdminResourceKind.PRINCIPAL, principal_id, tenant_id="tenant-a")

    assert principal.name == "Tenant User"
    assert admin.render_uix_view(AdminResourceKind.CREDENTIAL, tenant_id="tenant-a").state == AdminUiState.EMPTY


@pytest.mark.unit
def test_admin_t1_crud_for_all_control_plane_resource_types() -> None:
    admin, principal_id = _seed_control_plane()

    credential = admin.create_credential(
        actor="admin:root",
        tenant_id="tenant-a",
        principal_id=principal_id,
        name="Password",
        credential_kind="password",
    )
    app = admin.create_app(
        actor="admin:root",
        tenant_id="tenant-a",
        name="Portal",
        client_ids=("client-web",),
        owner_principal_id=principal_id,
    )
    service = admin.create_service_identity(
        actor="admin:root",
        tenant_id="tenant-a",
        name="Worker",
        scopes=("jobs.read", "jobs.write"),
        owner_principal_id=principal_id,
    )
    resource_server = admin.create_resource_server(
        actor="admin:root",
        tenant_id="tenant-a",
        name="Jobs API",
        audience="api://jobs",
        scopes=("jobs.read", "jobs.write"),
    )
    policy = admin.create_policy(
        actor="admin:root",
        tenant_id="tenant-a",
        name="Tenant Admin Policy",
        policy_kind="rbac",
        rules={"role": "tenant-admin", "permissions": ["tenant.*"]},
    )
    updated = admin.update(
        AdminResourceKind.APP,
        app.id,
        actor="admin:root",
        tenant_id="tenant-a",
        name="Portal App",
    )

    assert credential.principal_id == principal_id
    assert service.scopes == ("jobs.read", "jobs.write")
    assert resource_server.audience == "api://jobs"
    assert policy.rules["role"] == "tenant-admin"
    assert updated.name == "Portal App"
    assert [row.name for row in admin.list(AdminResourceKind.APP, tenant_id="tenant-a")] == ["Portal App"]


@pytest.mark.unit
def test_admin_t1_uix_ready_empty_loading_and_error_states() -> None:
    admin, principal_id = _seed_control_plane()

    ready = admin.render_uix_view(AdminResourceKind.PRINCIPAL, tenant_id="tenant-a")
    empty = admin.render_uix_view(AdminResourceKind.POLICY, tenant_id="tenant-a")
    loading = admin.render_uix_view(AdminResourceKind.APP, tenant_id="tenant-a", loading=True)
    error = admin.render_uix_view(AdminResourceKind.SERVICE_IDENTITY, tenant_id="tenant-a", error="failed")

    assert ready.state == AdminUiState.READY
    assert ready.rows[0].id == principal_id
    assert empty.is_empty is True
    assert loading.state == AdminUiState.LOADING
    assert error.state == AdminUiState.ERROR
    assert error.error == "failed"


@pytest.mark.unit
def test_admin_t2_tenant_isolation_delete_and_audit_guardrails() -> None:
    admin, principal_id = _seed_control_plane()
    policy = admin.create_policy(
        actor="admin:root",
        tenant_id="tenant-a",
        name="Policy",
        policy_kind="abac",
        rules={"region": "us-sw"},
    )

    with pytest.raises(AdminControlPlaneError, match="tenant mismatch"):
        admin.get(AdminResourceKind.PRINCIPAL, principal_id, tenant_id="tenant-b")

    deleted = admin.delete(AdminResourceKind.POLICY, policy.id, actor="admin:root", tenant_id="tenant-a")

    assert deleted.status == AdminResourceStatus.DELETED
    assert admin.render_uix_view(AdminResourceKind.POLICY, tenant_id="tenant-a").state == AdminUiState.EMPTY
    assert [(event.action, event.resource_kind) for event in admin.audit_events] == [
        ("create", AdminResourceKind.PRINCIPAL),
        ("create", AdminResourceKind.POLICY),
        ("delete", AdminResourceKind.POLICY),
    ]


@pytest.mark.unit
def test_admin_t2_public_boundary_has_no_forbidden_imports() -> None:
    files = [
        Path("pkgs/tigrbl-identity-admin/src/tigrbl_identity_admin/__init__.py"),
        Path("pkgs/tigrbl-identity-admin/src/tigrbl_identity_admin/control_plane.py"),
    ]
    forbidden = {
        "tigrbl_auth",
        "tigrbl_identity_server",
        "tigrbl_identity_runtime",
        "tigrbl_identity_operator",
    }

    imports: set[str] = set()
    for file in files:
        tree = ast.parse(file.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                imports.add(node.module.split(".")[0])

    assert imports.isdisjoint(forbidden)
