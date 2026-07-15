from __future__ import annotations

import ast
import asyncio
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
for src in (ROOT / "pkgs").rglob("src"):
    value = str(src)
    if value not in sys.path:
        sys.path.insert(0, value)

from tigrbl_identity_admin import (  # noqa: E402
    AdminControlPlane,
    AdminControlPlaneError,
    AdminResourceKind,
    AdminResourceStatus,
    App,
)
from tigrbl_identity_admin_control_plane import (  # noqa: E402
    AdminControlPlane as CanonicalAdminControlPlane,
)


class _MemoryAdminOperations:
    def __init__(self) -> None:
        self.records = {}
        self.audit_events = []

    def create(self, record):
        self.records[(record.metadata.kind, record.metadata.id)] = record

    def read(self, kind, resource_id):
        return self.records.get((kind, resource_id))

    def list(self, kind, tenant_id):
        return tuple(self.records.values())

    def update(self, record):
        self.create(record)

    def delete(self, record):
        self.create(record)

    def record_audit(self, event):
        self.audit_events.append(event)

    def list_audit(self):
        return tuple(self.audit_events)


def _new_control_plane() -> AdminControlPlane:
    operations = _MemoryAdminOperations()
    return AdminControlPlane(
        operations.create,
        operations.read,
        operations.list,
        operations.update,
        operations.delete,
        operations.record_audit,
        operations.list_audit,
    )


def _seed_control_plane() -> tuple[AdminControlPlane, str]:
    admin = _new_control_plane()
    principal = asyncio.run(
        admin.create_principal(
            actor="admin:root",
            tenant_id="tenant-a",
            subject="user:123",
            name="Tenant User",
            roles=("member",),
        )
    )
    return admin, principal.id


@pytest.mark.unit
def test_admin_t0_public_surfaces_are_importable() -> None:
    admin, principal_id = _seed_control_plane()

    principal = asyncio.run(
        admin.get(AdminResourceKind.PRINCIPAL, principal_id, tenant_id="tenant-a")
    )

    assert principal.display_name == "Tenant User"
    assert (
        asyncio.run(admin.list(AdminResourceKind.CREDENTIAL, tenant_id="tenant-a"))
        == ()
    )
    assert AdminControlPlane is CanonicalAdminControlPlane


@pytest.mark.unit
def test_admin_t1_crud_for_all_control_plane_resource_types() -> None:
    admin, principal_id = _seed_control_plane()

    credential = asyncio.run(
        admin.create_credential(
            actor="admin:root",
            tenant_id="tenant-a",
            principal_id=principal_id,
            name="Password",
            credential_kind="password",
        )
    )
    app = asyncio.run(
        admin.create_app(
            actor="admin:root",
            tenant_id="tenant-a",
            name="Portal",
            client_ids=("client-web",),
            owner_principal_id=principal_id,
        )
    )
    service = asyncio.run(
        admin.create_service_identity(
            actor="admin:root",
            tenant_id="tenant-a",
            name="Worker",
            scopes=("jobs.read", "jobs.write"),
            owner_principal_id=principal_id,
        )
    )
    resource_server = asyncio.run(
        admin.create_resource_server(
            actor="admin:root",
            tenant_id="tenant-a",
            name="Jobs API",
            audience="api://jobs",
            scopes=("jobs.read", "jobs.write"),
        )
    )
    policy = asyncio.run(
        admin.create_policy(
            actor="admin:root",
            tenant_id="tenant-a",
            name="Tenant Admin Policy",
            policy_kind="rbac",
            rules={"role": "tenant-admin", "permissions": ["tenant.*"]},
        )
    )
    updated = asyncio.run(
        admin.update(
            AdminResourceKind.APP,
            app.id,
            actor="admin:root",
            tenant_id="tenant-a",
            name="Portal App",
        )
    )

    assert credential.principal_id == principal_id
    assert isinstance(app, App)
    assert service.attributes["scopes"] == ("jobs.read", "jobs.write")
    assert resource_server.attributes["audience"] == "api://jobs"
    assert policy.language == "rbac"
    assert updated.name == "Portal App"
    assert [
        row.name
        for row in asyncio.run(admin.list(AdminResourceKind.APP, tenant_id="tenant-a"))
    ] == ["Portal App"]


@pytest.mark.unit
def test_admin_t1_lists_return_canonical_objects_without_uix_state_contracts() -> None:
    admin, principal_id = _seed_control_plane()

    principals = asyncio.run(
        admin.list(AdminResourceKind.PRINCIPAL, tenant_id="tenant-a")
    )
    policies = asyncio.run(admin.list(AdminResourceKind.POLICY, tenant_id="tenant-a"))

    assert principals[0].id == principal_id
    assert policies == ()
    assert not hasattr(admin, "render_uix_view")


@pytest.mark.unit
def test_admin_t2_tenant_isolation_delete_and_audit_guardrails() -> None:
    admin, principal_id = _seed_control_plane()
    policy = asyncio.run(
        admin.create_policy(
            actor="admin:root",
            tenant_id="tenant-a",
            name="Policy",
            policy_kind="abac",
            rules={"region": "us-sw"},
        )
    )

    with pytest.raises(AdminControlPlaneError, match="tenant mismatch"):
        asyncio.run(
            admin.get(
                AdminResourceKind.PRINCIPAL,
                principal_id,
                tenant_id="tenant-b",
            )
        )

    deleted = asyncio.run(
        admin.delete(
            AdminResourceKind.POLICY,
            policy.policy_id,
            actor="admin:root",
            tenant_id="tenant-a",
        )
    )

    assert deleted.status == AdminResourceStatus.DELETED
    assert asyncio.run(admin.list(AdminResourceKind.POLICY, tenant_id="tenant-a")) == ()
    assert [
        (event.action, event.resource_kind)
        for event in asyncio.run(admin.list_audit_events())
    ] == [
        ("create", AdminResourceKind.PRINCIPAL),
        ("create", AdminResourceKind.POLICY),
        ("delete", AdminResourceKind.POLICY),
    ]


@pytest.mark.unit
def test_admin_t2_public_boundary_has_no_forbidden_imports() -> None:
    files = [
        Path(
            "pkgs/40-capabilities/tigrbl-identity-admin-control-plane/src/tigrbl_identity_admin_control_plane/__init__.py"
        ),
        Path(
            "pkgs/40-capabilities/tigrbl-identity-admin-control-plane/src/tigrbl_identity_admin_control_plane/models.py"
        ),
        Path(
            "pkgs/40-capabilities/tigrbl-identity-admin-control-plane/src/tigrbl_identity_admin_control_plane/service.py"
        ),
        Path(
            "pkgs/20-providers/tigrbl-identity-admin/src/tigrbl_identity_admin/__init__.py"
        ),
        Path(
            "pkgs/20-providers/tigrbl-identity-admin/src/tigrbl_identity_admin/control_plane.py"
        ),
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
