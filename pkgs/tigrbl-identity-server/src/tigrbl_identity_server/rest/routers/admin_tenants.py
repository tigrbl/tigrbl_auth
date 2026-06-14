from __future__ import annotations

from uuid import UUID

from tigrbl_identity_server.framework import AsyncSession, Depends, HTTPException, Request, TigrblRouter, select, status
from tigrbl_identity_contracts.rest import AdminTenantOut, AdminTenantProvisionIn
from tigrbl_identity_admin.bootstrap import resolve_admin_user_from_request
from tigrbl_identity_storage.tables import Tenant, User
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


async def _require_admin(request: Request) -> User:
    actor = await resolve_admin_user_from_request(request)
    if actor is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "authenticated admin session required")
    return actor


def _uuid(value: str, *, label: str) -> UUID:
    try:
        return UUID(str(value))
    except Exception as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"invalid {label}") from exc


@api.route("/admin/tenant", methods=["GET"], response_model=list[AdminTenantOut])
async def admin_list_tenants(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    await _require_admin(request)
    rows = list(await db.scalars(select(Tenant).order_by(Tenant.created_at, Tenant.name, Tenant.slug)))
    return [_tenant_payload(row) for row in rows]


@api.route("/admin/tenant", methods=["POST"], response_model=AdminTenantOut)
async def admin_create_tenant(
    request: Request,
    payload: AdminTenantProvisionIn | None = None,
    db: AsyncSession = Depends(get_db),
):
    actor = await _require_admin(request)
    if not bool(getattr(actor, "is_superuser", False)):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "superuser privileges required to provision tenants")
    if payload is None:
        payload = AdminTenantProvisionIn.model_validate(await request.json() or {})

    slug = payload.slug.strip().lower()
    name = payload.name.strip()
    email = payload.email.strip().lower()

    existing = await db.scalar(select(Tenant).where((Tenant.slug == slug) | (Tenant.name == name) | (Tenant.email == email)))
    if existing is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, "tenant slug, name, or email already exists")

    row = Tenant(slug=slug, name=name, email=email)
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return _tenant_payload(row)


@api.route("/admin/tenant/{tenant_id}", methods=["DELETE"], response_model=AdminTenantOut)
async def admin_delete_tenant(
    request: Request,
    tenant_id: str,
    db: AsyncSession = Depends(get_db),
):
    actor = await _require_admin(request)
    if not bool(getattr(actor, "is_superuser", False)):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "superuser privileges required to delete tenants")

    row = await db.scalar(select(Tenant).where(Tenant.id == _uuid(tenant_id, label="tenant_id")))
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "tenant not found")
    if row.slug == "public":
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "cannot delete the default public tenant")
    if str(actor.tenant_id) == str(row.id):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "cannot delete the current administrator tenant")

    snapshot = _tenant_payload(row)
    await db.delete(row)
    await db.commit()
    return snapshot


__all__ = ["router", "api"]
