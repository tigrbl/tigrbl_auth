from __future__ import annotations

from typing import Any
from uuid import UUID

from tigrbl_identity_server.framework import Depends, HTTPException, Request, TigrblRouter, status
from tigrbl_identity_admin.bootstrap import resolve_admin_user_from_request
from tigrbl_identity_server.security.handler_records import (
    create_handler_record,
    delete_handler_record,
    first_handler_record,
    list_handler_records,
    read_handler_record,
    update_handler_record,
)
from tigrbl_identity_storage.tables import Tenant, User
from tigrbl_identity_storage.tables.tenant import (
    AdminTenantOut,
    AdminTenantProvisionIn,
    AdminTenantUpdateIn,
)
from tigrbl_identity_storage.tables.engine import get_db

api = router = TigrblRouter()


def _tenant_payload(row: Tenant) -> AdminTenantOut:
    return AdminTenantOut(
        id=str(row.id),
        slug=row.slug,
        name=row.name,
        email=row.email,
        created_at=getattr(row, "created_at", None).isoformat() if getattr(row, "created_at", None) else None,
        updated_at=getattr(row, "updated_at", None).isoformat() if getattr(row, "updated_at", None) else None,
    )


async def _require_admin(request: Request, db: Any) -> User:
    actor = await resolve_admin_user_from_request(request, db=db)
    if actor is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "authenticated admin session required")
    return actor


def _uuid(value: str, *, label: str) -> UUID:
    try:
        return UUID(str(value))
    except Exception as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"invalid {label}") from exc


async def _find_tenant_duplicate(db: Any, *, slug: str, name: str, email: str) -> Tenant | None:
    for filters in ({"slug": slug}, {"name": name}, {"email": email}):
        row = await first_handler_record(Tenant, db, filters)
        if row is not None:
            return row
    return None


@api.route("/admin/tenant", methods=["GET"], response_model=list[AdminTenantOut])
async def admin_list_tenants(
    request: Request,
    db: Any = Depends(get_db),
):
    await _require_admin(request, db)
    rows = await list_handler_records(Tenant, db)
    rows = sorted(rows, key=lambda row: (getattr(row, "created_at", None) or "", getattr(row, "name", ""), getattr(row, "slug", "")))
    return [_tenant_payload(row) for row in rows]


@api.route("/admin/tenant", methods=["POST"], response_model=AdminTenantOut)
async def admin_create_tenant(
    request: Request,
    payload: AdminTenantProvisionIn | None = None,
    db: Any = Depends(get_db),
):
    actor = await _require_admin(request, db)
    if not bool(getattr(actor, "is_superuser", False)):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "superuser privileges required to provision tenants")
    if payload is None:
        payload = AdminTenantProvisionIn.model_validate(await request.json() or {})

    slug = payload.slug.strip().lower()
    name = payload.name.strip()
    email = payload.email.strip().lower()

    existing = await _find_tenant_duplicate(db, slug=slug, name=name, email=email)
    if existing is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, "tenant slug, name, or email already exists")

    row = await create_handler_record(Tenant, db, {"slug": slug, "name": name, "email": email})
    return _tenant_payload(row)


@api.route("/admin/tenant/{tenant_id}", methods=["DELETE"], response_model=AdminTenantOut)
async def admin_delete_tenant(
    request: Request,
    tenant_id: str,
    db: Any = Depends(get_db),
):
    actor = await _require_admin(request, db)
    if not bool(getattr(actor, "is_superuser", False)):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "superuser privileges required to delete tenants")

    row = await read_handler_record(Tenant, db, _uuid(tenant_id, label="tenant_id"))
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "tenant not found")
    if row.slug == "public":
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "cannot delete the default public tenant")
    if str(actor.tenant_id) == str(row.id):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "cannot delete the current administrator tenant")

    snapshot = _tenant_payload(row)
    await delete_handler_record(Tenant, db, row.id)
    return snapshot


@api.route("/admin/tenant/{tenant_id}", methods=["PATCH"], response_model=AdminTenantOut)
async def admin_update_tenant(
    request: Request,
    tenant_id: str,
    payload: AdminTenantUpdateIn | None = None,
    db: Any = Depends(get_db),
):
    actor = await _require_admin(request, db)
    if not bool(getattr(actor, "is_superuser", False)):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "superuser privileges required to update tenants")
    if payload is None:
        payload = AdminTenantUpdateIn.model_validate(await request.json() or {})

    row = await read_handler_record(Tenant, db, _uuid(tenant_id, label="tenant_id"))
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "tenant not found")
    changes: dict[str, Any] = {}
    if payload.realm_id is not None:
        changes["realm_id"] = _uuid(payload.realm_id, label="realm_id")
    if payload.slug is not None:
        changes["slug"] = payload.slug.strip().lower()
    if payload.name is not None:
        changes["name"] = payload.name.strip()
    if payload.email is not None:
        changes["email"] = payload.email.strip().lower()
    if payload.is_active is not None:
        changes["is_active"] = payload.is_active
    if changes:
        duplicate = await _find_tenant_duplicate(
            db,
            slug=changes.get("slug", row.slug),
            name=changes.get("name", row.name),
            email=changes.get("email", row.email),
        )
        if duplicate is not None and str(duplicate.id) != str(row.id):
            raise HTTPException(status.HTTP_409_CONFLICT, "tenant slug, name, or email already exists")
        row = await update_handler_record(Tenant, db, row.id, changes)
    return _tenant_payload(row)


__all__ = ["router", "api", "admin_update_tenant"]
