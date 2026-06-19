"""My-account routes bound to the User storage table."""

from __future__ import annotations

import datetime as dt
import uuid
from datetime import timezone
from typing import Any

from tigrbl_identity_server.framework import Depends, Header, HTTPException, Request, status
from tigrbl_identity_jose.key_management import hash_pw

from .._ops import read_record, update_record
from ..engine import get_db
from ._table import (
    MY_ACCOUNT_TAGS,
    MyAccountMutationOut,
    MyAccountPasswordChangeIn,
    MyAccountProfileOut,
    MyAccountProfileUpdateIn,
    User,
    account_api,
)


def _not_found_uuid(value: str, *, field: str) -> uuid.UUID:
    try:
        return uuid.UUID(str(value))
    except ValueError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"{field} not found") from exc


def _iso(value: dt.datetime | None) -> str | None:
    if value is None:
        return None
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.isoformat()


async def _current_principal_dependency(
    request: Request,
    authorization: str = Header("", alias="Authorization"),
    api_key: str | None = Header(None, alias="x-api-key"),
    dpop: str | None = Header(None, alias="DPoP"),
    db: Any = Depends(get_db),
) -> User:
    from tigrbl_identity_server.security.auth import get_current_principal

    return await get_current_principal(request, authorization=authorization, api_key=api_key, dpop=dpop, db=db)


def _profile_payload(user: User) -> MyAccountProfileOut:
    return MyAccountProfileOut(
        id=str(user.id),
        tenant_id=str(user.tenant_id),
        username=str(user.username),
        email=str(user.email),
        is_active=bool(user.is_active),
        must_change_password=bool(getattr(user, "must_change_password", False)),
        roles=list(getattr(user, "roles", ())),
        created_at=_iso(getattr(user, "created_at", None)),
        updated_at=_iso(getattr(user, "updated_at", None)),
    )


async def _current_user_row(current_user: User, db: Any) -> User:
    row = await read_record(User, db, current_user.id)
    if row is not None and str(getattr(row, "tenant_id", "")) != str(current_user.tenant_id):
        row = None
    if row is not None and not bool(getattr(row, "is_active", True)):
        row = None
    if row is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "authenticated account required")
    return row


@account_api.route(
    "/account/profile",
    methods=["GET"],
    response_model=MyAccountProfileOut,
    tags=MY_ACCOUNT_TAGS,
)
async def get_account_profile(
    current_user: User = Depends(_current_principal_dependency),
    db: Any = Depends(get_db),
) -> MyAccountProfileOut:
    return _profile_payload(await _current_user_row(current_user, db))


@account_api.route(
    "/account/profile",
    methods=["PATCH"],
    response_model=MyAccountProfileOut,
    tags=MY_ACCOUNT_TAGS,
)
async def update_account_profile(
    request: Request,
    payload: MyAccountProfileUpdateIn | None = None,
    current_user: User = Depends(_current_principal_dependency),
    db: Any = Depends(get_db),
) -> MyAccountProfileOut:
    if payload is None:
        payload = MyAccountProfileUpdateIn.model_validate(await request.json() or {})
    row = await _current_user_row(current_user, db)
    changes = {name: value for name in ("username", "email") if (value := getattr(payload, name)) is not None}
    if changes:
        row = await update_record(User, db, row.id, changes)
    return _profile_payload(row)


@account_api.route(
    "/account/password/change",
    methods=["POST"],
    response_model=MyAccountMutationOut,
    tags=MY_ACCOUNT_TAGS,
)
async def change_account_password(
    request: Request,
    payload: MyAccountPasswordChangeIn | None = None,
    current_user: User = Depends(_current_principal_dependency),
    db: Any = Depends(get_db),
) -> MyAccountMutationOut:
    if payload is None:
        payload = MyAccountPasswordChangeIn.model_validate(await request.json() or {})
    row = await _current_user_row(current_user, db)
    if not row.verify_password(payload.current_password):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "invalid current password")
    row = await update_record(
        User,
        db,
        row.id,
        {
            "password_hash": hash_pw(payload.new_password),
            "must_change_password": False,
            "password_reset_token_hash": None,
            "password_reset_expires_at": None,
        },
    )
    return MyAccountMutationOut(status="changed", id=str(row.id))


__all__ = [
    "_current_principal_dependency",
    "_iso",
    "_not_found_uuid",
    "change_account_password",
    "get_account_profile",
    "update_account_profile",
]
