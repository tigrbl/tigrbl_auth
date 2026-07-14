"""Platform tenant-administration HTTP routes."""

from __future__ import annotations

import uuid
from typing import Any

from pydantic import BaseModel, constr
from tigrbl import TigrblRouter
from tigrbl.requests import Request
from tigrbl.runtime.status import HTTPException
from tigrbl.security import Depends
from tigrbl_authz_policy_admin_gate import ADMIN_OPENAPI_SECURITY_DEPENDENCIES
from tigrbl_identity_storage.tables import Tenant
from tigrbl_identity_storage_runtime.engine import get_db
from tigrbl_identity_storage_runtime.ops.common import (
    create_table_record,
    delete_table_record,
    field_value,
    first_table_record,
    list_table_records,
    read_table_record,
    update_table_record,
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


def tenant_payload(row: Any) -> AdminTenantOut:
    created_at = field_value(row, "created_at")
    updated_at = field_value(row, "updated_at")
    realm_id = field_value(row, "realm_id")
    return AdminTenantOut(
        id=str(field_value(row, "id")),
        realm_id=str(realm_id) if realm_id else None,
        slug=str(field_value(row, "slug")),
        name=str(field_value(row, "name")),
        email=str(field_value(row, "email")),
        created_at=created_at.isoformat() if created_at else None,
        updated_at=updated_at.isoformat() if updated_at else None,
    )


async def _require_admin(request: Request, db: Any) -> Any:
    from tigrbl_identity_admin.bootstrap import resolve_admin_user_from_request

    actor = await resolve_admin_user_from_request(request, db=db)
    if actor is None:
        raise HTTPException(401, "authenticated admin session required")
    return actor


def _require_superuser(actor: Any, action: str) -> None:
    if not bool(getattr(actor, "is_superuser", False)):
        raise HTTPException(403, f"superuser privileges required to {action} tenants")


def _uuid(value: str, *, label: str) -> uuid.UUID:
    try:
        return uuid.UUID(str(value))
    except (TypeError, ValueError) as exc:
        raise HTTPException(400, f"invalid {label}") from exc


async def _find_duplicate(db: Any, *, slug: str, name: str, email: str) -> Any:
    for filters in ({"slug": slug}, {"name": name}, {"email": email}):
        row = await first_table_record(Tenant, db, filters)
        if row is not None:
            return row
    return None


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
    await _require_admin(request, db)
    rows = await list_table_records(Tenant, db)
    rows = sorted(
        rows,
        key=lambda row: (
            field_value(row, "created_at") or "",
            field_value(row, "name", ""),
            field_value(row, "slug", ""),
        ),
    )
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
    actor = await _require_admin(request, db)
    _require_superuser(actor, "provision")
    if payload is None:
        payload = AdminTenantProvisionIn.model_validate(await request.json() or {})
    slug = payload.slug.strip().lower()
    name = payload.name.strip()
    email = payload.email.strip().lower()
    if await _find_duplicate(db, slug=slug, name=name, email=email):
        raise HTTPException(409, "tenant slug, name, or email already exists")
    row = await create_table_record(
        Tenant,
        db,
        {
            "realm_id": _uuid(payload.realm_id, label="realm_id")
            if payload.realm_id is not None
            else None,
            "slug": slug,
            "name": name,
            "email": email,
        },
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
    actor = await _require_admin(request, db)
    _require_superuser(actor, "delete")
    row = await read_table_record(Tenant, db, _uuid(tenant_id, label="tenant_id"))
    if row is None:
        raise HTTPException(404, "tenant not found")
    if field_value(row, "slug") == "public":
        raise HTTPException(400, "cannot delete the default public tenant")
    if str(actor.tenant_id) == str(field_value(row, "id")):
        raise HTTPException(400, "cannot delete the current administrator tenant")
    snapshot = tenant_payload(row)
    await delete_table_record(Tenant, db, field_value(row, "id"))
    return snapshot


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
    actor = await _require_admin(request, db)
    _require_superuser(actor, "update")
    if payload is None:
        payload = AdminTenantUpdateIn.model_validate(await request.json() or {})
    row = await read_table_record(Tenant, db, _uuid(tenant_id, label="tenant_id"))
    if row is None:
        raise HTTPException(404, "tenant not found")
    changes: dict[str, Any] = {}
    if payload.realm_id is not None:
        changes["realm_id"] = _uuid(payload.realm_id, label="realm_id")
    if payload.slug is not None:
        changes["slug"] = payload.slug.strip().lower()
    if payload.name is not None:
        changes["name"] = payload.name.strip()
    if payload.email is not None:
        changes["email"] = payload.email.strip().lower()
    if payload.is_active is not None:
        changes["is_active"] = payload.is_active
    if changes:
        duplicate = await _find_duplicate(
            db,
            slug=changes.get("slug", field_value(row, "slug")),
            name=changes.get("name", field_value(row, "name")),
            email=changes.get("email", field_value(row, "email")),
        )
        if duplicate is not None and str(field_value(duplicate, "id")) != str(
            field_value(row, "id")
        ):
            raise HTTPException(409, "tenant slug, name, or email already exists")
        row = await update_table_record(Tenant, db, field_value(row, "id"), changes)
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
