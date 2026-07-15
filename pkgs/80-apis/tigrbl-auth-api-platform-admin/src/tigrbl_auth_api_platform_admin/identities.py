"""Platform identity-administration HTTP routes."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, constr
from tigrbl import TigrblRouter
from tigrbl.requests import Request
from tigrbl.runtime.status import HTTPException
from tigrbl.security import Depends
from tigrbl_identity_contracts.admin_identities import (
    AdminIdentity,
    AdminIdentityCreate,
    AdminIdentityUpdate,
    IdentityAdministrationConflictError,
    IdentityAdministrationNotFoundError,
    IdentityAdministrationPolicyError,
    IdentityAdministrationValidationError,
)
from tigrbl_identity_contracts.admin_tenants import (
    TenantAdministratorAuthenticationError,
)
from tigrbl_identity_server.platform_identity_administration import (
    get_db,
    identity_administration_for_request,
    require_identity_administrator,
)
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


def _identity_payload(row: AdminIdentity) -> AdminIdentityOut:
    return AdminIdentityOut(
        id=row.identity_id,
        tenant_id=row.tenant_id,
        username=row.username,
        email=row.email,
        is_active=row.is_active,
        is_admin=row.is_admin,
        is_superuser=row.is_superuser,
        must_change_password=row.must_change_password,
        roles=list(row.roles),
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


async def _invoke(
    request: Request,
    db: Any,
    operation: str,
    *args: object,
) -> object:
    try:
        actor = await require_identity_administrator(request, db)
        capability = identity_administration_for_request(request, db)
        return (await capability.call(operation, actor, *args)).value
    except TenantAdministratorAuthenticationError as exc:
        raise HTTPException(401, str(exc)) from exc
    except IdentityAdministrationPolicyError as exc:
        raise HTTPException(403, str(exc)) from exc
    except IdentityAdministrationNotFoundError as exc:
        raise HTTPException(404, str(exc)) from exc
    except IdentityAdministrationConflictError as exc:
        raise HTTPException(409, str(exc)) from exc
    except IdentityAdministrationValidationError as exc:
        raise HTTPException(400, str(exc)) from exc


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
    rows = await _invoke(request, db, "list_identities", tenant_id)
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
    if payload is None:
        payload = AdminIdentityProvisionIn.model_validate(await request.json() or {})
    row = await _invoke(
        request,
        db,
        "create_identity",
        AdminIdentityCreate(
            tenant_id=payload.tenant_id,
            username=payload.username,
            email=str(payload.email),
            password=payload.password,
            is_admin=payload.is_admin,
            is_superuser=payload.is_superuser,
            must_change_password=payload.must_change_password,
        ),
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
    if payload is None:
        payload = AdminIdentityUpdateIn.model_validate(await request.json() or {})
    row = await _invoke(
        request,
        db,
        "update_identity",
        user_id,
        AdminIdentityUpdate(
            username=payload.username,
            email=str(payload.email) if payload.email is not None else None,
            password=payload.password,
            is_active=payload.is_active,
            is_admin=payload.is_admin,
            is_superuser=payload.is_superuser,
            must_change_password=payload.must_change_password,
        ),
    )
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
    row = await _invoke(request, db, "delete_identity", user_id)
    return _identity_payload(row)


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
