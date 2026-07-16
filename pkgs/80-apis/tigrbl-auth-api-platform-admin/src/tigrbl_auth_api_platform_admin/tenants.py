"""Platform tenant-administration HTTP routes."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, constr
from tigrbl import TigrblRouter
from tigrbl.requests import Request
from tigrbl.runtime.status import HTTPException
from tigrbl.security import Depends
from tigrbl_auth_api_admin_gate import ADMIN_OPENAPI_SECURITY_DEPENDENCIES
from tigrbl_identity_contracts.admin_tenants import (
    AdminTenant,
    AdminTenantCreate,
    AdminTenantUpdate,
    TenantAdministrationConflictError,
    TenantAdministrationNotFoundError,
    TenantAdministrationPolicyError,
    TenantAdministrationValidationError,
    TenantAdministratorAuthenticationError,
)
from tigrbl_identity_server.platform_tenant_administration import (
    get_db,
    require_tenant_administrator,
    tenant_administration_for_request,
)


_email = constr(strip_whitespace=True, min_length=3, max_length=120)
_name = constr(strip_whitespace=True, min_length=1, max_length=120)
_slug = constr(strip_whitespace=True, min_length=3, max_length=120)
_SECURITY = list(ADMIN_OPENAPI_SECURITY_DEPENDENCIES)


class AdminTenantOut(BaseModel):
    id: str
    realm_id: str | None = None
    slug: str
    name: str
    email: str
    created_at: str | None = None
    updated_at: str | None = None


class AdminTenantProvisionIn(BaseModel):
    realm_id: str | None = None
    slug: _slug
    name: _name
    email: _email


class AdminTenantUpdateIn(BaseModel):
    realm_id: str | None = None
    slug: _slug | None = None
    name: _name | None = None
    email: _email | None = None
    is_active: bool | None = None


def tenant_payload(row: AdminTenant) -> AdminTenantOut:
    return AdminTenantOut(
        id=row.tenant_id,
        realm_id=row.realm_id,
        slug=row.slug,
        name=row.name,
        email=row.email,
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
        actor = await require_tenant_administrator(request, db)
        capability = tenant_administration_for_request(request, db)
        return (await capability.call(operation, actor, *args)).value
    except TenantAdministratorAuthenticationError as exc:
        raise HTTPException(401, str(exc)) from exc
    except TenantAdministrationPolicyError as exc:
        raise HTTPException(403, str(exc)) from exc
    except TenantAdministrationNotFoundError as exc:
        raise HTTPException(404, str(exc)) from exc
    except TenantAdministrationConflictError as exc:
        raise HTTPException(409, str(exc)) from exc
    except TenantAdministrationValidationError as exc:
        raise HTTPException(400, str(exc)) from exc


api = admin_router = router = TigrblRouter()


@router.route(
    "/admin/tenant",
    methods=["GET"],
    response_model=list[AdminTenantOut],
    dependencies=_SECURITY,
)
async def admin_list_tenants(
    request: Request,
    db: Any = Depends(get_db),
) -> list[AdminTenantOut]:
    rows = await _invoke(request, db, "list_tenants")
    return [tenant_payload(row) for row in rows]


@router.route(
    "/admin/tenant",
    methods=["POST"],
    response_model=AdminTenantOut,
    dependencies=_SECURITY,
)
async def admin_create_tenant(
    request: Request,
    payload: AdminTenantProvisionIn | None = None,
    db: Any = Depends(get_db),
) -> AdminTenantOut:
    if payload is None:
        payload = AdminTenantProvisionIn.model_validate(await request.json() or {})
    row = await _invoke(
        request,
        db,
        "create_tenant",
        AdminTenantCreate(
            realm_id=payload.realm_id,
            slug=payload.slug,
            name=payload.name,
            email=payload.email,
        ),
    )
    return tenant_payload(row)


@router.route(
    "/admin/tenant/{tenant_id}",
    methods=["DELETE"],
    response_model=AdminTenantOut,
    dependencies=_SECURITY,
)
async def admin_delete_tenant(
    request: Request,
    tenant_id: str,
    db: Any = Depends(get_db),
) -> AdminTenantOut:
    row = await _invoke(request, db, "delete_tenant", tenant_id)
    return tenant_payload(row)


@router.route(
    "/admin/tenant/{tenant_id}",
    methods=["PATCH"],
    response_model=AdminTenantOut,
    dependencies=_SECURITY,
)
async def admin_update_tenant(
    request: Request,
    tenant_id: str,
    payload: AdminTenantUpdateIn | None = None,
    db: Any = Depends(get_db),
) -> AdminTenantOut:
    if payload is None:
        payload = AdminTenantUpdateIn.model_validate(await request.json() or {})
    row = await _invoke(
        request,
        db,
        "update_tenant",
        tenant_id,
        AdminTenantUpdate(
            realm_id=payload.realm_id,
            slug=payload.slug,
            name=payload.name,
            email=payload.email,
            is_active=payload.is_active,
        ),
    )
    return tenant_payload(row)


__all__ = [
    "AdminTenantOut",
    "AdminTenantProvisionIn",
    "AdminTenantUpdateIn",
    "admin_create_tenant",
    "admin_delete_tenant",
    "admin_list_tenants",
    "admin_router",
    "admin_update_tenant",
    "api",
    "router",
    "tenant_payload",
]
