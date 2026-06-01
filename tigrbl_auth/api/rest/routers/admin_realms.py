from __future__ import annotations

from uuid import UUID

from tigrbl_auth.api.rest.schemas import AdminRealmOut, AdminRealmProvisionIn, AdminRealmUpdateIn, AdminTenantOut, AdminTenantProvisionIn
from tigrbl_auth.framework import AsyncSession, Depends, HTTPException, Request, TigrblRouter, select, status
from tigrbl_auth.services.admin_identity_bootstrap import resolve_admin_user_from_request
from tigrbl_auth.tables import Realm, Tenant, User
from tigrbl_auth.tables.engine import get_db

api = router = TigrblRouter()


def _realm_payload(row: Realm) -> AdminRealmOut:
    return AdminRealmOut(
        id=str(row.id),
        slug=row.slug,
        name=row.name,
        issuer_path=row.issuer_path,
        description=row.description,
        created_at=getattr(row, "created_at", None).isoformat() if getattr(row, "created_at", None) else None,
        updated_at=getattr(row, "updated_at", None).isoformat() if getattr(row, "updated_at", None) else None,
    )


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


async def _require_superuser(request: Request) -> User:
    actor = await resolve_admin_user_from_request(request)
    if actor is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "authenticated admin session required")
    if not bool(getattr(actor, "is_superuser", False)):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "superuser privileges required")
    return actor


def _uuid(value: str, *, label: str) -> UUID:
    try:
        return UUID(str(value))
    except Exception as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"invalid {label}") from exc


def _issuer_path(value: str | None, slug: str) -> str:
    text = (value if value is not None else f"/realms/{slug}").strip()
    if text == "":
        return ""
    if not text.startswith("/"):
        text = f"/{text}"
    return text.rstrip("/")


@api.route("/admin/realm", methods=["GET"], response_model=list[AdminRealmOut])
async def admin_list_realms(request: Request, db: AsyncSession = Depends(get_db)):
    await _require_superuser(request)
    rows = list(await db.scalars(select(Realm).order_by(Realm.created_at, Realm.name, Realm.slug)))
    return [_realm_payload(row) for row in rows]


@api.route("/admin/realm", methods=["POST"], response_model=AdminRealmOut)
async def admin_create_realm(
    request: Request,
    payload: AdminRealmProvisionIn | None = None,
    db: AsyncSession = Depends(get_db),
):
    await _require_superuser(request)
    if payload is None:
        payload = AdminRealmProvisionIn.model_validate(await request.json() or {})
    slug = payload.slug.strip().lower()
    name = payload.name.strip()
    issuer_path = _issuer_path(payload.issuer_path, slug)
    existing = await db.scalar(select(Realm).where((Realm.slug == slug) | (Realm.name == name) | (Realm.issuer_path == issuer_path)))
    if existing is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, "realm slug, name, or issuer path already exists")
    row = Realm(slug=slug, name=name, issuer_path=issuer_path, description=payload.description)
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return _realm_payload(row)


@api.route("/admin/realm/{realm_id}", methods=["GET"], response_model=AdminRealmOut)
async def admin_get_realm(request: Request, realm_id: str, db: AsyncSession = Depends(get_db)):
    await _require_superuser(request)
    row = await db.scalar(select(Realm).where(Realm.id == _uuid(realm_id, label="realm_id")))
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "realm not found")
    return _realm_payload(row)


@api.route("/admin/realm/{realm_id}", methods=["PATCH"], response_model=AdminRealmOut)
async def admin_update_realm(
    request: Request,
    realm_id: str,
    payload: AdminRealmUpdateIn | None = None,
    db: AsyncSession = Depends(get_db),
):
    await _require_superuser(request)
    if payload is None:
        payload = AdminRealmUpdateIn.model_validate(await request.json() or {})
    row = await db.scalar(select(Realm).where(Realm.id == _uuid(realm_id, label="realm_id")))
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "realm not found")
    if payload.slug is not None:
        row.slug = payload.slug.strip().lower()
    if payload.name is not None:
        row.name = payload.name.strip()
    if payload.issuer_path is not None:
        row.issuer_path = _issuer_path(payload.issuer_path, row.slug)
    if payload.description is not None:
        row.description = payload.description
    await db.commit()
    await db.refresh(row)
    return _realm_payload(row)


@api.route("/admin/realm/{realm_id}", methods=["DELETE"], response_model=AdminRealmOut)
async def admin_delete_realm(request: Request, realm_id: str, db: AsyncSession = Depends(get_db)):
    await _require_superuser(request)
    row = await db.scalar(select(Realm).where(Realm.id == _uuid(realm_id, label="realm_id")))
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "realm not found")
    tenant_count = len(list(await db.scalars(select(Tenant).where(Tenant.realm_id == row.id))))
    if tenant_count:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "cannot delete a realm that still owns tenants")
    snapshot = _realm_payload(row)
    await db.delete(row)
    await db.commit()
    return snapshot


@api.route("/admin/realm/{realm_id}/tenant", methods=["GET"], response_model=list[AdminTenantOut])
async def admin_list_realm_tenants(request: Request, realm_id: str, db: AsyncSession = Depends(get_db)):
    await _require_superuser(request)
    rid = _uuid(realm_id, label="realm_id")
    rows = list(await db.scalars(select(Tenant).where(Tenant.realm_id == rid).order_by(Tenant.created_at, Tenant.name, Tenant.slug)))
    return [_tenant_payload(row) for row in rows]


@api.route("/admin/realm/{realm_id}/tenant", methods=["POST"], response_model=AdminTenantOut)
async def admin_create_realm_tenant(
    request: Request,
    realm_id: str,
    payload: AdminTenantProvisionIn | None = None,
    db: AsyncSession = Depends(get_db),
):
    await _require_superuser(request)
    if payload is None:
        payload = AdminTenantProvisionIn.model_validate(await request.json() or {})
    realm = await db.scalar(select(Realm).where(Realm.id == _uuid(realm_id, label="realm_id")))
    if realm is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "realm not found")
    slug = payload.slug.strip().lower()
    name = payload.name.strip()
    email = payload.email.strip().lower()
    existing = await db.scalar(select(Tenant).where((Tenant.slug == slug) | (Tenant.name == name) | (Tenant.email == email)))
    if existing is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, "tenant slug, name, or email already exists")
    row = Tenant(slug=slug, name=name, email=email, realm_id=realm.id)
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return _tenant_payload(row)


__all__ = ["router", "api"]
