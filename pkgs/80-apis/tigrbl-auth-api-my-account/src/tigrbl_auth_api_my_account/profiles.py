"""Current-subject profile and password routes."""

from __future__ import annotations

import datetime as dt
from datetime import timezone
from typing import Any

from pydantic import BaseModel, Field, constr
from tigrbl import TigrblRouter
from tigrbl.requests import Request
from tigrbl.runtime.status import HTTPException
from tigrbl.security import Depends
from tigrbl_identity_storage.tables import User
from tigrbl_identity_storage.tables.engine import get_db
from tigrbl_identity_storage_runtime.ops.common import (
    field_value,
    read_table_record,
    update_table_record,
)
from tigrbl_secret_hashing_bcrypt_provider import BcryptSecretHasher

from .common import MyAccountMutationOut, current_principal_dependency


_email = constr(strip_whitespace=True, min_length=3, max_length=120)
_password = constr(min_length=8, max_length=256)
_username = constr(strip_whitespace=True, min_length=3, max_length=80)


class MyAccountProfileOut(BaseModel):
    id: str
    tenant_id: str
    username: str
    email: str
    is_active: bool = True
    must_change_password: bool = False
    roles: list[str] = Field(default_factory=list)
    created_at: str | None = None
    updated_at: str | None = None


class MyAccountProfileUpdateIn(BaseModel):
    username: _username | None = None
    email: _email | None = None


class MyAccountPasswordChangeIn(BaseModel):
    current_password: _password
    new_password: _password


def _iso(value: dt.datetime | None) -> str | None:
    if value is None:
        return None
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.isoformat()


def _profile_payload(user: Any) -> MyAccountProfileOut:
    return MyAccountProfileOut(
        id=str(field_value(user, "id")),
        tenant_id=str(field_value(user, "tenant_id")),
        username=str(field_value(user, "username")),
        email=str(field_value(user, "email")),
        is_active=bool(field_value(user, "is_active", True)),
        must_change_password=bool(field_value(user, "must_change_password", False)),
        roles=list(field_value(user, "roles", ())),
        created_at=_iso(field_value(user, "created_at")),
        updated_at=_iso(field_value(user, "updated_at")),
    )


async def _current_user_row(current_user: User, db: Any) -> Any:
    row = await read_table_record(User, db, current_user.id)
    if row is not None and str(field_value(row, "tenant_id", "")) != str(
        current_user.tenant_id
    ):
        row = None
    if row is not None and not bool(field_value(row, "is_active", True)):
        row = None
    if row is None:
        raise HTTPException(401, "authenticated account required")
    return row


api = router = TigrblRouter()
MY_ACCOUNT_TAGS = ["My Account"]


@api.route(
    "/account/profile",
    methods=["GET"],
    response_model=MyAccountProfileOut,
    tags=MY_ACCOUNT_TAGS,
)
async def get_account_profile(
    request: Request | None = None,
    current_user: User | None = None,
    db: Any = Depends(get_db),
) -> MyAccountProfileOut:
    if current_user is None:
        if request is None:
            raise HTTPException(401, "authenticated account required")
        current_user = await current_principal_dependency(request, db=db)
    return _profile_payload(await _current_user_row(current_user, db))


@api.route(
    "/account/profile",
    methods=["PATCH"],
    response_model=MyAccountProfileOut,
    tags=MY_ACCOUNT_TAGS,
)
async def update_account_profile(
    request: Request | None = None,
    payload: MyAccountProfileUpdateIn | None = None,
    current_user: User | None = None,
    db: Any = Depends(get_db),
) -> MyAccountProfileOut:
    if current_user is None:
        if request is None:
            raise HTTPException(401, "authenticated account required")
        current_user = await current_principal_dependency(request, db=db)
    if payload is None:
        if request is None:
            raise HTTPException(400, "request payload required")
        payload = MyAccountProfileUpdateIn.model_validate(await request.json() or {})
    row = await _current_user_row(current_user, db)
    changes = {
        name: value
        for name in ("username", "email")
        if (value := getattr(payload, name)) is not None
    }
    if changes:
        row = await update_table_record(User, db, field_value(row, "id"), changes)
    return _profile_payload(row)


@api.route(
    "/account/password/change",
    methods=["POST"],
    response_model=MyAccountMutationOut,
    tags=MY_ACCOUNT_TAGS,
)
async def change_account_password(
    request: Request | None = None,
    payload: MyAccountPasswordChangeIn | None = None,
    current_user: User | None = None,
    db: Any = Depends(get_db),
) -> MyAccountMutationOut:
    if current_user is None:
        if request is None:
            raise HTTPException(401, "authenticated account required")
        current_user = await current_principal_dependency(request, db=db)
    if payload is None:
        if request is None:
            raise HTTPException(400, "request payload required")
        payload = MyAccountPasswordChangeIn.model_validate(await request.json() or {})
    row = await _current_user_row(current_user, db)
    hasher = BcryptSecretHasher()
    verification = hasher.verify_secret(
        payload.current_password,
        field_value(row, "password_hash"),
    )
    if not verification.verified:
        raise HTTPException(400, "invalid current password")
    encoded = hasher.hash_secret(payload.new_password).encoded
    row = await update_table_record(
        User,
        db,
        field_value(row, "id"),
        {
            "password_hash": encoded,
            "must_change_password": False,
            "password_reset_token_hash": None,
            "password_reset_expires_at": None,
        },
    )
    return MyAccountMutationOut(status="changed", id=str(field_value(row, "id")))


__all__ = [
    "MyAccountPasswordChangeIn",
    "MyAccountProfileOut",
    "MyAccountProfileUpdateIn",
    "api",
    "change_account_password",
    "get_account_profile",
    "router",
    "update_account_profile",
]
