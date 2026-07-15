"""Platform realm-administration HTTP routes."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, constr
from tigrbl import TigrblRouter
from tigrbl.requests import Request
from tigrbl.runtime.status import HTTPException
from tigrbl.security import Depends
from tigrbl_authz_policy_admin_gate import ADMIN_OPENAPI_SECURITY_DEPENDENCIES
from tigrbl_identity_contracts.admin_realms import (
    AdminRealm,
    AdminRealmCreate,
    AdminRealmUpdate,
    RealmAdministrationConflictError,
    RealmAdministrationNotFoundError,
    RealmAdministrationValidationError,
)
from tigrbl_identity_contracts.admin_tenants import (
    AdminTenantCreate,
    TenantAdministrationConflictError,
    TenantAdministrationNotFoundError,
    TenantAdministrationPolicyError,
    TenantAdministrationValidationError,
    TenantAdministratorAuthenticationError,
)
from tigrbl_identity_server.platform_realm_administration import (
    get_db,
    realm_administration_for_request,
    require_realm_administrator,
)

from .tenants import AdminTenantOut, AdminTenantProvisionIn, tenant_payload


_description = constr(strip_whitespace=True, max_length=255)
_issuer_path_value = constr(strip_whitespace=True, max_length=255)
_name = constr(strip_whitespace=True, min_length=1, max_length=120)
_slug = constr(strip_whitespace=True, min_length=3, max_length=120)
_SECURITY = list(ADMIN_OPENAPI_SECURITY_DEPENDENCIES)


class AdminRealmOut(BaseModel):
    id: str
    slug: str
    name: str
    issuer_path: str = ""
    description: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class AdminRealmProvisionIn(BaseModel):
    slug: _slug
    name: _name
    issuer_path: _issuer_path_value | None = None
    description: _description | None = None


class AdminRealmUpdateIn(BaseModel):
    slug: _slug | None = None
    name: _name | None = None
    issuer_path: _issuer_path_value | None = None
    description: _description | None = None


def _realm_payload(row: AdminRealm) -> AdminRealmOut:
    return AdminRealmOut(
        id=row.realm_id,
        slug=row.slug,
        name=row.name,
        issuer_path=row.issuer_path,
        description=row.description,
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
        actor = await require_realm_administrator(request, db)
        capability = realm_administration_for_request(request, db)
        return (await capability.call(operation, actor, *args)).value
    except TenantAdministratorAuthenticationError as exc:
        raise HTTPException(401, str(exc)) from exc
    except TenantAdministrationPolicyError as exc:
        raise HTTPException(403, str(exc)) from exc
    except (RealmAdministrationNotFoundError, TenantAdministrationNotFoundError) as exc:
        raise HTTPException(404, str(exc)) from exc
    except (RealmAdministrationConflictError, TenantAdministrationConflictError) as exc:
        raise HTTPException(409, str(exc)) from exc
    except (
        RealmAdministrationValidationError,
        TenantAdministrationValidationError,
    ) as exc:
        raise HTTPException(400, str(exc)) from exc


api = router = TigrblRouter()


@api.route(
    "/admin/realm",
    methods=["GET"],
    response_model=list[AdminRealmOut],
    dependencies=_SECURITY,
)
async def admin_list_realms(
    request: Request,
    db: Any = Depends(get_db),
) -> list[AdminRealmOut]:
    rows = await _invoke(request, db, "list_realms")
    return [_realm_payload(row) for row in rows]


@api.route(
    "/admin/realm",
    methods=["POST"],
    response_model=AdminRealmOut,
    dependencies=_SECURITY,
)
async def admin_create_realm(
    request: Request,
    payload: AdminRealmProvisionIn | None = None,
    db: Any = Depends(get_db),
) -> AdminRealmOut:
    if payload is None:
        payload = AdminRealmProvisionIn.model_validate(await request.json() or {})
    row = await _invoke(
        request,
        db,
        "create_realm",
        AdminRealmCreate(
            slug=payload.slug,
            name=payload.name,
            issuer_path=payload.issuer_path,
            description=payload.description,
        ),
    )
    return _realm_payload(row)


@api.route(
    "/admin/realm/{realm_id}",
    methods=["GET"],
    response_model=AdminRealmOut,
    dependencies=_SECURITY,
)
async def admin_get_realm(
    request: Request,
    realm_id: str,
    db: Any = Depends(get_db),
) -> AdminRealmOut:
    row = await _invoke(request, db, "read_realm", realm_id)
    if row is None:
        raise HTTPException(404, "realm not found")
    return _realm_payload(row)


@api.route(
    "/admin/realm/{realm_id}",
    methods=["PATCH"],
    response_model=AdminRealmOut,
    dependencies=_SECURITY,
)
async def admin_update_realm(
    request: Request,
    realm_id: str,
    payload: AdminRealmUpdateIn | None = None,
    db: Any = Depends(get_db),
) -> AdminRealmOut:
    if payload is None:
        payload = AdminRealmUpdateIn.model_validate(await request.json() or {})
    row = await _invoke(
        request,
        db,
        "update_realm",
        realm_id,
        AdminRealmUpdate(
            slug=payload.slug,
            name=payload.name,
            issuer_path=payload.issuer_path,
            description=payload.description,
        ),
    )
    return _realm_payload(row)


@api.route(
    "/admin/realm/{realm_id}",
    methods=["DELETE"],
    response_model=AdminRealmOut,
    dependencies=_SECURITY,
)
async def admin_delete_realm(
    request: Request,
    realm_id: str,
    db: Any = Depends(get_db),
) -> AdminRealmOut:
    row = await _invoke(request, db, "delete_realm", realm_id)
    return _realm_payload(row)


@api.route(
    "/admin/realm/{realm_id}/tenant",
    methods=["GET"],
    response_model=list[AdminTenantOut],
    dependencies=_SECURITY,
)
async def admin_list_realm_tenants(
    request: Request,
    realm_id: str,
    db: Any = Depends(get_db),
) -> list[AdminTenantOut]:
    rows = await _invoke(request, db, "list_realm_tenants", realm_id)
    return [tenant_payload(row) for row in rows]


@api.route(
    "/admin/realm/{realm_id}/tenant",
    methods=["POST"],
    response_model=AdminTenantOut,
    dependencies=_SECURITY,
)
async def admin_create_realm_tenant(
    request: Request,
    realm_id: str,
    payload: AdminTenantProvisionIn | None = None,
    db: Any = Depends(get_db),
) -> AdminTenantOut:
    if payload is None:
        payload = AdminTenantProvisionIn.model_validate(await request.json() or {})
    row = await _invoke(
        request,
        db,
        "create_realm_tenant",
        realm_id,
        AdminTenantCreate(
            realm_id=realm_id,
            slug=payload.slug,
            name=payload.name,
            email=payload.email,
        ),
    )
    return tenant_payload(row)


__all__ = [
    "AdminRealmOut",
    "AdminRealmProvisionIn",
    "AdminRealmUpdateIn",
    "admin_create_realm",
    "admin_create_realm_tenant",
    "admin_delete_realm",
    "admin_get_realm",
    "admin_list_realm_tenants",
    "admin_list_realms",
    "admin_update_realm",
    "api",
    "router",
]
