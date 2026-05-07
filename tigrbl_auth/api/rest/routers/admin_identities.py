from __future__ import annotations

from uuid import UUID

from tigrbl_auth.framework import AsyncSession, Depends, HTTPException, Request, TigrblRouter, select, status
from tigrbl_auth.api.rest.schemas import (
    AdminIdentityOut,
    AdminIdentityProvisionIn,
    AdminIdentityUpdateIn,
)
from tigrbl_auth.services.admin_identity_bootstrap import resolve_admin_user_from_request
from tigrbl_auth.services.key_management import hash_pw
from tigrbl_auth.tables import Tenant, User
from tigrbl_auth.tables.engine import get_db

api = router = TigrblRouter()


def _identity_payload(row: User) -> AdminIdentityOut:
    return AdminIdentityOut(
        id=str(row.id),
        tenant_id=str(row.tenant_id),
        username=row.username,
        email=row.email,
        is_active=bool(getattr(row, "is_active", True)),
        is_admin=bool(getattr(row, "is_admin", False)),
        is_superuser=bool(getattr(row, "is_superuser", False)),
        must_change_password=bool(getattr(row, "must_change_password", False)),
        roles=list(getattr(row, "roles", ())),
        created_at=getattr(row, "created_at", None).isoformat() if getattr(row, "created_at", None) else None,
        updated_at=getattr(row, "updated_at", None).isoformat() if getattr(row, "updated_at", None) else None,
    )


async def _require_admin(request: Request) -> User:
    actor = await resolve_admin_user_from_request(request)
    if actor is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "authenticated admin session required")
    return actor


def _check_admin_escalation(actor: User, *, target_admin: bool, target_superuser: bool) -> None:
    if target_superuser and not bool(getattr(actor, "is_superuser", False)):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "superuser privileges required")
    if target_admin and not bool(getattr(actor, "is_superuser", False)):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "superuser privileges required to onboard administrators")


def _uuid(value: str, *, label: str) -> UUID:
    try:
        return UUID(str(value))
    except Exception as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"invalid {label}") from exc


@api.route("/admin/identities", methods=["GET"], response_model=list[AdminIdentityOut])
async def admin_list_identities(
    request: Request,
    tenant_id: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    actor = await _require_admin(request)
    query = select(User)
    effective_tenant_id = _uuid(tenant_id or str(actor.tenant_id), label="tenant_id")
    query = query.where(User.tenant_id == effective_tenant_id)
    rows = list(await db.scalars(query.order_by(User.created_at)))
    return [_identity_payload(row) for row in rows]


@api.route("/admin/identities", methods=["POST"], response_model=AdminIdentityOut)
async def admin_create_identity(
    request: Request,
    payload: AdminIdentityProvisionIn | None = None,
    db: AsyncSession = Depends(get_db),
):
    actor = await _require_admin(request)
    if payload is None:
        payload = AdminIdentityProvisionIn.model_validate(await request.json() or {})
    _check_admin_escalation(
        actor,
        target_admin=bool(payload.is_admin),
        target_superuser=bool(payload.is_superuser),
    )
    tenant = await db.scalar(select(Tenant).where(Tenant.id == _uuid(payload.tenant_id, label="tenant_id")))
    if tenant is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "tenant not found")
    existing = await db.scalar(select(User).where((User.username == payload.username) | (User.email == payload.email)))
    if existing is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, "username or email already exists")

    row = User(
        tenant_id=tenant.id,
        username=payload.username,
        email=str(payload.email),
        password_hash=hash_pw(payload.password),
        is_admin=bool(payload.is_admin),
        is_superuser=bool(payload.is_superuser),
        must_change_password=bool(payload.must_change_password),
    )
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return _identity_payload(row)


@api.route("/admin/identities/{user_id}", methods=["PATCH"], response_model=AdminIdentityOut)
async def admin_update_identity(
    request: Request,
    user_id: str,
    payload: AdminIdentityUpdateIn | None = None,
    db: AsyncSession = Depends(get_db),
):
    actor = await _require_admin(request)
    if payload is None:
        payload = AdminIdentityUpdateIn.model_validate(await request.json() or {})
    row = await db.scalar(select(User).where(User.id == _uuid(user_id, label="user_id")))
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")

    next_is_admin = bool(payload.is_admin) if payload.is_admin is not None else bool(getattr(row, "is_admin", False))
    next_is_superuser = bool(payload.is_superuser) if payload.is_superuser is not None else bool(getattr(row, "is_superuser", False))
    _check_admin_escalation(actor, target_admin=next_is_admin, target_superuser=next_is_superuser)
    if str(actor.id) == str(row.id) and payload.is_active is False:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "cannot deactivate the current administrator")

    if payload.username is not None:
        row.username = payload.username
    if payload.email is not None:
        row.email = str(payload.email)
    if payload.password is not None:
        row.password_hash = hash_pw(payload.password)
    if payload.is_active is not None:
        row.is_active = payload.is_active
    if payload.is_admin is not None:
        row.is_admin = payload.is_admin
    if payload.is_superuser is not None:
        row.is_superuser = payload.is_superuser
    if payload.must_change_password is not None:
        row.must_change_password = payload.must_change_password
    await db.commit()
    await db.refresh(row)
    return _identity_payload(row)


@api.route("/admin/identities/{user_id}", methods=["DELETE"], response_model=AdminIdentityOut)
async def admin_delete_identity(
    request: Request,
    user_id: str,
    db: AsyncSession = Depends(get_db),
):
    actor = await _require_admin(request)
    row = await db.scalar(select(User).where(User.id == _uuid(user_id, label="user_id")))
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")
    if str(actor.id) == str(row.id):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "cannot delete the current administrator")
    if bool(getattr(row, "is_superuser", False)) and not bool(getattr(actor, "is_superuser", False)):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "superuser privileges required")
    snapshot = _identity_payload(row)
    await db.delete(row)
    await db.commit()
    return snapshot


__all__ = ["router", "api"]
