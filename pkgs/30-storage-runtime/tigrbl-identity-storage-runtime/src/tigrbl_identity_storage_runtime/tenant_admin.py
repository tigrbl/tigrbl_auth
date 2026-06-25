from __future__ import annotations

import uuid
from typing import Any

from tigrbl_identity_storage.framework import Depends, HTTPException, Request, TigrblRouter, status
from tigrbl_identity_storage.tables.engine import get_db
from tigrbl_identity_storage.tables.tenant import AdminTenantOut, AdminTenantProvisionIn, AdminTenantUpdateIn, Tenant

admin_router = router = TigrblRouter()


def _tenant_payload(row: Tenant) -> AdminTenantOut:
    return AdminTenantOut(
        id=str(row.id),
        realm_id=str(row.realm_id) if getattr(row, "realm_id", None) else None,
        slug=row.slug,
        name=row.name,
        email=row.email,
        created_at=getattr(row, "created_at", None).isoformat() if getattr(row, "created_at", None) else None,
        updated_at=getattr(row, "updated_at", None).isoformat() if getattr(row, "updated_at", None) else None,
    )


def _items(result: Any) -> list[Any]:
    if isinstance(result, dict) and isinstance(result.get("items"), list):
        return result["items"]
    if isinstance(result, list):
        return result
    if isinstance(result, tuple):
        return list(result)
    return [] if result is None else [result]


async def _require_admin(request: Request, db: Any) -> Any:
    from tigrbl_identity_admin.bootstrap import resolve_admin_user_from_request

    actor = await resolve_admin_user_from_request(request, db=db)
    if actor is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "authenticated admin session required")
    return actor


def _uuid(value: str, *, label: str) -> uuid.UUID:
    try:
        return uuid.UUID(str(value))
    except Exception as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"invalid {label}") from exc


async def _find_tenant_duplicate(db: Any, *, slug: str, name: str, email: str) -> Tenant | None:
    for filters in ({"slug": slug}, {"name": name}, {"email": email}):
        rows = _items(await Tenant.handlers.list.core({"payload": {"filters": filters}, "db": db}))
        if rows:
            return rows[0]
    return None


@router.route("/admin/tenant", methods=["GET"], response_model=list[AdminTenantOut])
async def admin_list_tenants(request: Request, db: Any = Depends(get_db)) -> list[AdminTenantOut]:
    await _require_admin(request, db)
    rows = _items(await Tenant.handlers.list.core({"payload": {}, "db": db}))
    rows = sorted(
        rows,
        key=lambda row: (
            getattr(row, "created_at", None) or "",
            getattr(row, "name", ""),
            getattr(row, "slug", ""),
        ),
    )
    return [_tenant_payload(row) for row in rows]


@router.route("/admin/tenant", methods=["POST"], response_model=AdminTenantOut)
async def admin_create_tenant(
    request: Request,
    payload: AdminTenantProvisionIn | None = None,
    db: Any = Depends(get_db),
) -> AdminTenantOut:
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
    row = await Tenant.handlers.create.core(
        {
            "payload": {
                "realm_id": _uuid(payload.realm_id, label="realm_id") if payload.realm_id is not None else None,
                "slug": slug,
                "name": name,
                "email": email,
            },
            "db": db,
        }
    )
    return _tenant_payload(row)


@router.route("/admin/tenant/{tenant_id}", methods=["DELETE"], response_model=AdminTenantOut)
async def admin_delete_tenant(request: Request, tenant_id: str, db: Any = Depends(get_db)) -> AdminTenantOut:
    actor = await _require_admin(request, db)
    if not bool(getattr(actor, "is_superuser", False)):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "superuser privileges required to delete tenants")
    row = await Tenant.handlers.read.core({"path_params": {"id": _uuid(tenant_id, label="tenant_id")}, "db": db})
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "tenant not found")
    if row.slug == "public":
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "cannot delete the default public tenant")
    if str(actor.tenant_id) == str(row.id):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "cannot delete the current administrator tenant")
    snapshot = _tenant_payload(row)
    await Tenant.handlers.delete.core({"path_params": {"id": row.id}, "db": db})
    return snapshot


@router.route("/admin/tenant/{tenant_id}", methods=["PATCH"], response_model=AdminTenantOut)
async def admin_update_tenant(
    request: Request,
    tenant_id: str,
    payload: AdminTenantUpdateIn | None = None,
    db: Any = Depends(get_db),
) -> AdminTenantOut:
    actor = await _require_admin(request, db)
    if not bool(getattr(actor, "is_superuser", False)):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "superuser privileges required to update tenants")
    if payload is None:
        payload = AdminTenantUpdateIn.model_validate(await request.json() or {})
    row = await Tenant.handlers.read.core({"path_params": {"id": _uuid(tenant_id, label="tenant_id")}, "db": db})
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
        row = await Tenant.handlers.update.core({"path_params": {"id": row.id}, "payload": changes, "db": db})
    return _tenant_payload(row)


__all__ = [
    "admin_router",
    "router",
    "admin_create_tenant",
    "admin_delete_tenant",
    "admin_list_tenants",
    "admin_update_tenant",
]
