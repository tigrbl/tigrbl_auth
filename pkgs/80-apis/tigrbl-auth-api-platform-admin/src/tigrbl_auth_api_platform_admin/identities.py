"""Platform identity-administration HTTP routes."""

from __future__ import annotations

import uuid
from typing import Any

from pydantic import BaseModel, Field, constr
from tigrbl import TigrblRouter
from tigrbl.requests import Request
from tigrbl.runtime.status import HTTPException
from tigrbl.security import Depends
from tigrbl_identity_storage.tables import Tenant, User
from tigrbl_identity_storage.tables.engine import get_db
from tigrbl_identity_storage_runtime.ops.common import (
    create_table_record,
    delete_table_record,
    field_value,
    first_table_record,
    list_table_records,
    read_table_record,
    update_table_record,
)
from tigrbl_secret_hashing_bcrypt_provider import BcryptSecretHasher
from tigrbl_authz_policy_admin_gate import ADMIN_OPENAPI_SECURITY_DEPENDENCIES


_email = constr(strip_whitespace=True, min_length=3, max_length=120)
_password = constr(min_length=8, max_length=256)
_username = constr(strip_whitespace=True, min_length=3, max_length=80)


class AdminIdentityOut(BaseModel):
    id: str
    tenant_id: str
    username: str
    email: str
    is_active: bool = True
    is_admin: bool = False
    is_superuser: bool = False
    must_change_password: bool = False
    roles: list[str] = Field(default_factory=list)
    created_at: str | None = None
    updated_at: str | None = None


class AdminIdentityProvisionIn(BaseModel):
    tenant_id: str
    username: _username
    email: _email
    password: _password
    is_admin: bool = False
    is_superuser: bool = False
    must_change_password: bool = True


class AdminIdentityUpdateIn(BaseModel):
    username: _username | None = None
    email: _email | None = None
    password: _password | None = None
    is_active: bool | None = None
    is_admin: bool | None = None
    is_superuser: bool | None = None
    must_change_password: bool | None = None


def _identity_payload(row: Any) -> AdminIdentityOut:
    created_at = field_value(row, "created_at")
    updated_at = field_value(row, "updated_at")
    return AdminIdentityOut(
        id=str(field_value(row, "id")),
        tenant_id=str(field_value(row, "tenant_id")),
        username=str(field_value(row, "username")),
        email=str(field_value(row, "email")),
        is_active=bool(field_value(row, "is_active", True)),
        is_admin=bool(field_value(row, "is_admin", False)),
        is_superuser=bool(field_value(row, "is_superuser", False)),
        must_change_password=bool(field_value(row, "must_change_password", False)),
        roles=list(field_value(row, "roles", ())),
        created_at=created_at.isoformat() if created_at else None,
        updated_at=updated_at.isoformat() if updated_at else None,
    )


async def _require_admin(request: Request, db: Any) -> User:
    from tigrbl_identity_admin.bootstrap import resolve_admin_user_from_request

    actor = await resolve_admin_user_from_request(request, db=db)
    if actor is None:
        raise HTTPException(401, "authenticated admin session required")
    return actor


def _check_admin_escalation(
    actor: User,
    *,
    target_admin: bool,
    target_superuser: bool,
) -> None:
    if target_superuser and not bool(getattr(actor, "is_superuser", False)):
        raise HTTPException(403, "superuser privileges required")
    if target_admin and not bool(getattr(actor, "is_superuser", False)):
        raise HTTPException(403, "superuser privileges required to onboard administrators")


def _uuid(value: str, *, label: str) -> uuid.UUID:
    try:
        return uuid.UUID(str(value))
    except (TypeError, ValueError) as exc:
        raise HTTPException(400, f"invalid {label}") from exc


api = router = TigrblRouter()


@api.route(
    "/admin/identities",
    methods=["GET"],
    response_model=list[AdminIdentityOut],
    dependencies=list(ADMIN_OPENAPI_SECURITY_DEPENDENCIES),
)
async def admin_list_identities(
    request: Request,
    tenant_id: str | None = None,
    db: Any = Depends(get_db),
) -> list[AdminIdentityOut]:
    actor = await _require_admin(request, db)
    effective_tenant_id = _uuid(tenant_id or str(actor.tenant_id), label="tenant_id")
    rows = await list_table_records(User, db, {"tenant_id": effective_tenant_id})
    rows = sorted(rows, key=lambda row: field_value(row, "created_at") or "")
    return [_identity_payload(row) for row in rows]


@api.route(
    "/admin/identities",
    methods=["POST"],
    response_model=AdminIdentityOut,
    dependencies=list(ADMIN_OPENAPI_SECURITY_DEPENDENCIES),
)
async def admin_create_identity(
    request: Request,
    payload: AdminIdentityProvisionIn | None = None,
    db: Any = Depends(get_db),
) -> AdminIdentityOut:
    actor = await _require_admin(request, db)
    if payload is None:
        payload = AdminIdentityProvisionIn.model_validate(await request.json() or {})
    _check_admin_escalation(
        actor,
        target_admin=bool(payload.is_admin),
        target_superuser=bool(payload.is_superuser),
    )
    tenant = await read_table_record(Tenant, db, _uuid(payload.tenant_id, label="tenant_id"))
    if tenant is None:
        raise HTTPException(404, "tenant not found")
    existing = await first_table_record(User, db, {"username": payload.username})
    if existing is None:
        existing = await first_table_record(User, db, {"email": str(payload.email)})
    if existing is not None:
        raise HTTPException(409, "username or email already exists")
    password_hash = BcryptSecretHasher().hash_secret(payload.password).encoded
    row = await create_table_record(
        User,
        db,
        {
            "tenant_id": field_value(tenant, "id"),
            "username": payload.username,
            "email": str(payload.email),
            "password_hash": password_hash,
            "is_admin": bool(payload.is_admin),
            "is_superuser": bool(payload.is_superuser),
            "must_change_password": bool(payload.must_change_password),
        },
    )
    return _identity_payload(row)


@api.route(
    "/admin/identities/{user_id}",
    methods=["PATCH"],
    response_model=AdminIdentityOut,
    dependencies=list(ADMIN_OPENAPI_SECURITY_DEPENDENCIES),
)
async def admin_update_identity(
    request: Request,
    user_id: str,
    payload: AdminIdentityUpdateIn | None = None,
    db: Any = Depends(get_db),
) -> AdminIdentityOut:
    actor = await _require_admin(request, db)
    if payload is None:
        payload = AdminIdentityUpdateIn.model_validate(await request.json() or {})
    row = await read_table_record(User, db, _uuid(user_id, label="user_id"))
    if row is None:
        raise HTTPException(404, "user not found")
    next_is_admin = (
        bool(payload.is_admin)
        if payload.is_admin is not None
        else bool(field_value(row, "is_admin", False))
    )
    next_is_superuser = (
        bool(payload.is_superuser)
        if payload.is_superuser is not None
        else bool(field_value(row, "is_superuser", False))
    )
    _check_admin_escalation(
        actor,
        target_admin=next_is_admin,
        target_superuser=next_is_superuser,
    )
    if str(actor.id) == str(field_value(row, "id")) and payload.is_active is False:
        raise HTTPException(400, "cannot deactivate the current administrator")
    changes: dict[str, Any] = {}
    for field_name in (
        "username",
        "is_active",
        "is_admin",
        "is_superuser",
        "must_change_password",
    ):
        value = getattr(payload, field_name)
        if value is not None:
            changes[field_name] = value
    if payload.email is not None:
        changes["email"] = str(payload.email)
    if payload.password is not None:
        changes["password_hash"] = BcryptSecretHasher().hash_secret(payload.password).encoded
    if changes:
        row = await update_table_record(User, db, field_value(row, "id"), changes)
    return _identity_payload(row)


@api.route(
    "/admin/identities/{user_id}",
    methods=["DELETE"],
    response_model=AdminIdentityOut,
    dependencies=list(ADMIN_OPENAPI_SECURITY_DEPENDENCIES),
)
async def admin_delete_identity(
    request: Request,
    user_id: str,
    db: Any = Depends(get_db),
) -> AdminIdentityOut:
    actor = await _require_admin(request, db)
    row = await read_table_record(User, db, _uuid(user_id, label="user_id"))
    if row is None:
        raise HTTPException(404, "user not found")
    if str(actor.id) == str(field_value(row, "id")):
        raise HTTPException(400, "cannot delete the current administrator")
    if bool(field_value(row, "is_superuser", False)) and not bool(
        getattr(actor, "is_superuser", False)
    ):
        raise HTTPException(403, "superuser privileges required")
    snapshot = _identity_payload(row)
    await delete_table_record(User, db, field_value(row, "id"))
    return snapshot


__all__ = [
    "AdminIdentityOut",
    "AdminIdentityProvisionIn",
    "AdminIdentityUpdateIn",
    "admin_create_identity",
    "admin_delete_identity",
    "admin_list_identities",
    "admin_update_identity",
    "api",
    "router",
]
