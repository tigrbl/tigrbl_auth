"""Current-subject profile and password HTTP routes."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, constr
from tigrbl import TigrblRouter
from tigrbl.requests import Request
from tigrbl.runtime.status import HTTPException
from tigrbl.security import Depends
from tigrbl_identity_contracts.account_self_service import (
    AccountAuthenticationError,
    AccountPrincipal,
    AccountProfile,
    AccountProfileUpdate,
    AccountValidationError,
)
from tigrbl_identity_server.account_self_service import (
    account_principal,
    account_self_service_for_request,
    get_db,
)

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


def _profile_payload(profile: AccountProfile) -> MyAccountProfileOut:
    return MyAccountProfileOut(
        id=profile.identity_id,
        tenant_id=profile.tenant_id,
        username=profile.username,
        email=profile.email,
        is_active=profile.is_active,
        must_change_password=profile.must_change_password,
        roles=list(profile.roles),
        created_at=profile.created_at,
        updated_at=profile.updated_at,
    )


async def _principal(
    request: Request | None, current_user: object | None, db: object
) -> AccountPrincipal:
    if current_user is not None:
        return account_principal(current_user)
    if request is None:
        raise HTTPException(401, "authenticated account required")
    return await current_principal_dependency(request, db=db)


def _capability(request: Request | None, db: object):
    return (
        account_self_service_for_request(request, db)
        if request
        else account_self_service_for_request(object(), db)
    )


def _raise_http(exc: Exception) -> None:
    if isinstance(exc, AccountAuthenticationError):
        raise HTTPException(401, str(exc)) from exc
    if isinstance(exc, AccountValidationError):
        raise HTTPException(400, str(exc)) from exc
    raise exc


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
    current_user: object | None = None,
    db: Any = Depends(get_db),
) -> MyAccountProfileOut:
    principal = await _principal(request, current_user, db)
    try:
        return _profile_payload(await _capability(request, db).get_profile(principal))
    except (AccountAuthenticationError, AccountValidationError) as exc:
        _raise_http(exc)


@api.route(
    "/account/profile",
    methods=["PATCH"],
    response_model=MyAccountProfileOut,
    tags=MY_ACCOUNT_TAGS,
)
async def update_account_profile(
    request: Request | None = None,
    payload: MyAccountProfileUpdateIn | None = None,
    current_user: object | None = None,
    db: Any = Depends(get_db),
) -> MyAccountProfileOut:
    principal = await _principal(request, current_user, db)
    if payload is None:
        if request is None:
            raise HTTPException(400, "request payload required")
        payload = MyAccountProfileUpdateIn.model_validate(await request.json() or {})
    try:
        profile = await _capability(request, db).update_profile(
            principal, AccountProfileUpdate(payload.username, payload.email)
        )
        return _profile_payload(profile)
    except (AccountAuthenticationError, AccountValidationError) as exc:
        _raise_http(exc)


@api.route(
    "/account/password/change",
    methods=["POST"],
    response_model=MyAccountMutationOut,
    tags=MY_ACCOUNT_TAGS,
)
async def change_account_password(
    request: Request | None = None,
    payload: MyAccountPasswordChangeIn | None = None,
    current_user: object | None = None,
    db: Any = Depends(get_db),
) -> MyAccountMutationOut:
    principal = await _principal(request, current_user, db)
    if payload is None:
        if request is None:
            raise HTTPException(400, "request payload required")
        payload = MyAccountPasswordChangeIn.model_validate(await request.json() or {})
    try:
        result = await _capability(request, db).change_password(
            principal, payload.current_password, payload.new_password
        )
        return MyAccountMutationOut(status=result.status, id=result.resource_id)
    except (AccountAuthenticationError, AccountValidationError) as exc:
        _raise_http(exc)


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
