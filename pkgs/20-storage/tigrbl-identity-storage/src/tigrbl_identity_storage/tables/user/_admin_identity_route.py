"""Admin identity routes bound to the User storage table."""

from __future__ import annotations

import uuid
from typing import Any

from tigrbl_identity_server.framework import Depends, HTTPException, Request, status
from tigrbl_identity_jose.key_management import hash_pw

from .._ops import create_record, delete_record, first_record, list_records, read_record, update_record
from ..engine import get_db
from ._table import AdminIdentityOut, AdminIdentityProvisionIn, AdminIdentityUpdateIn, User, admin_api


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


async def _require_admin(request: Request, db: Any) -> User:
    from tigrbl_identity_admin.bootstrap import resolve_admin_user_from_request

    actor = await resolve_admin_user_from_request(request, db=db)
    if actor is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "authenticated admin session required")
    return actor


def _check_admin_escalation(actor: User, *, target_admin: bool, target_superuser: bool) -> None:
    if target_superuser and not bool(getattr(actor, "is_superuser", False)):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "superuser privileges required")
    if target_admin and not bool(getattr(actor, "is_superuser", False)):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "superuser privileges required to onboard administrators")


def _uuid(value: str, *, label: str) -> uuid.UUID:
    try:
        return uuid.UUID(str(value))
    except Exception as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"invalid {label}") from exc


@admin_api.route("/admin/identities", methods=["GET"], response_model=list[AdminIdentityOut])
async def admin_list_identities(
    request: Request,
    tenant_id: str | None = None,
    db: Any = Depends(get_db),
) -> list[AdminIdentityOut]:
    actor = await _require_admin(request, db)
    effective_tenant_id = _uuid(tenant_id or str(actor.tenant_id), label="tenant_id")
    rows = await list_records(User, db, {"tenant_id": effective_tenant_id})
    rows = sorted(rows, key=lambda row: getattr(row, "created_at", None) or "")
    return [_identity_payload(row) for row in rows]


@admin_api.route("/admin/identities", methods=["POST"], response_model=AdminIdentityOut)
async def admin_create_identity(
    request: Request,
    payload: AdminIdentityProvisionIn | None = None,
    db: Any = Depends(get_db),
) -> AdminIdentityOut:
    from ..tenant import Tenant

    actor = await _require_admin(request, db)
    if payload is None:
        payload = AdminIdentityProvisionIn.model_validate(await request.json() or {})
    _check_admin_escalation(actor, target_admin=bool(payload.is_admin), target_superuser=bool(payload.is_superuser))
    tenant = await read_record(Tenant, db, _uuid(payload.tenant_id, label="tenant_id"))
    if tenant is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "tenant not found")
    existing = await first_record(User, db, {"username": payload.username})
    if existing is None:
        existing = await first_record(User, db, {"email": str(payload.email)})
    if existing is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, "username or email already exists")

    row = await create_record(
        User,
        db,
        {
            "tenant_id": tenant.id,
            "username": payload.username,
            "email": str(payload.email),
            "password_hash": hash_pw(payload.password),
            "is_admin": bool(payload.is_admin),
            "is_superuser": bool(payload.is_superuser),
            "must_change_password": bool(payload.must_change_password),
        },
    )
    return _identity_payload(row)


@admin_api.route("/admin/identities/{user_id}", methods=["PATCH"], response_model=AdminIdentityOut)
async def admin_update_identity(
    request: Request,
    user_id: str,
    payload: AdminIdentityUpdateIn | None = None,
    db: Any = Depends(get_db),
) -> AdminIdentityOut:
    actor = await _require_admin(request, db)
    if payload is None:
        payload = AdminIdentityUpdateIn.model_validate(await request.json() or {})
    row = await read_record(User, db, _uuid(user_id, label="user_id"))
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")

    next_is_admin = bool(payload.is_admin) if payload.is_admin is not None else bool(getattr(row, "is_admin", False))
    next_is_superuser = (
        bool(payload.is_superuser) if payload.is_superuser is not None else bool(getattr(row, "is_superuser", False))
    )
    _check_admin_escalation(actor, target_admin=next_is_admin, target_superuser=next_is_superuser)
    if str(actor.id) == str(row.id) and payload.is_active is False:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "cannot deactivate the current administrator")

    changes: dict[str, Any] = {}
    for field_name in ("username", "is_active", "is_admin", "is_superuser", "must_change_password"):
        value = getattr(payload, field_name)
        if value is not None:
            changes[field_name] = value
    if payload.email is not None:
        changes["email"] = str(payload.email)
    if payload.password is not None:
        changes["password_hash"] = hash_pw(payload.password)
    if changes:
        row = await update_record(User, db, row.id, changes)
    return _identity_payload(row)


@admin_api.route("/admin/identities/{user_id}", methods=["DELETE"], response_model=AdminIdentityOut)
async def admin_delete_identity(request: Request, user_id: str, db: Any = Depends(get_db)) -> AdminIdentityOut:
    actor = await _require_admin(request, db)
    row = await read_record(User, db, _uuid(user_id, label="user_id"))
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")
    if str(actor.id) == str(row.id):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "cannot delete the current administrator")
    if bool(getattr(row, "is_superuser", False)) and not bool(getattr(actor, "is_superuser", False)):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "superuser privileges required")
    snapshot = _identity_payload(row)
    await delete_record(User, db, row.id)
    return snapshot


__all__ = [
    "admin_create_identity",
    "admin_delete_identity",
    "admin_list_identities",
    "admin_update_identity",
]
