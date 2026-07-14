"""Platform realm-administration HTTP routes."""

from __future__ import annotations

import uuid
from typing import Any

from pydantic import BaseModel, constr
from tigrbl import TigrblRouter
from tigrbl.requests import Request
from tigrbl.runtime.status import HTTPException
from tigrbl.security import Depends
from tigrbl_authz_policy_admin_gate import ADMIN_OPENAPI_SECURITY_DEPENDENCIES
from tigrbl_identity_storage.tables import Realm, Tenant
from tigrbl_identity_storage_runtime.engine import get_db
from .tenants import AdminTenantOut, AdminTenantProvisionIn, tenant_payload
from tigrbl_identity_storage_runtime.ops.common import (
    create_table_record,
    delete_table_record,
    field_value,
    first_table_record,
    list_table_records,
    read_table_record,
    update_table_record,
)


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


def _realm_payload(row: Any) -> AdminRealmOut:
    created_at = field_value(row, "created_at")
    updated_at = field_value(row, "updated_at")
    return AdminRealmOut(
        id=str(field_value(row, "id")),
        slug=str(field_value(row, "slug")),
        name=str(field_value(row, "name")),
        issuer_path=str(field_value(row, "issuer_path", "")),
        description=field_value(row, "description"),
        created_at=created_at.isoformat() if created_at else None,
        updated_at=updated_at.isoformat() if updated_at else None,
    )


async def _require_superuser(request: Request, db: Any) -> Any:
    from tigrbl_identity_admin.bootstrap import resolve_admin_user_from_request

    actor = await resolve_admin_user_from_request(request, db=db)
    if actor is None:
        raise HTTPException(401, "authenticated admin session required")
    if not bool(getattr(actor, "is_superuser", False)):
        raise HTTPException(403, "superuser privileges required")
    return actor


def _uuid(value: str, *, label: str) -> uuid.UUID:
    try:
        return uuid.UUID(str(value))
    except (TypeError, ValueError) as exc:
        raise HTTPException(400, f"invalid {label}") from exc


def _issuer_path(value: str | None, slug: str) -> str:
    text = (value if value is not None else f"/realms/{slug}").strip()
    if not text:
        return ""
    if not text.startswith("/"):
        text = f"/{text}"
    return text.rstrip("/")


async def _find_realm_duplicate(
    db: Any,
    *,
    slug: str,
    name: str,
    issuer_path: str,
) -> Any:
    for filters in ({"slug": slug}, {"name": name}, {"issuer_path": issuer_path}):
        row = await first_table_record(Realm, db, filters)
        if row is not None:
            return row
    return None


async def _find_tenant_duplicate(
    db: Any,
    *,
    slug: str,
    name: str,
    email: str,
) -> Any:
    for filters in ({"slug": slug}, {"name": name}, {"email": email}):
        row = await first_table_record(Tenant, db, filters)
        if row is not None:
            return row
    return None


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
    await _require_superuser(request, db)
    rows = await list_table_records(Realm, db)
    rows = sorted(
        rows,
        key=lambda row: (
            field_value(row, "created_at") or "",
            field_value(row, "name", ""),
            field_value(row, "slug", ""),
        ),
    )
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
    await _require_superuser(request, db)
    if payload is None:
        payload = AdminRealmProvisionIn.model_validate(await request.json() or {})
    slug = payload.slug.strip().lower()
    name = payload.name.strip()
    issuer_path = _issuer_path(payload.issuer_path, slug)
    if await _find_realm_duplicate(db, slug=slug, name=name, issuer_path=issuer_path):
        raise HTTPException(409, "realm slug, name, or issuer path already exists")
    row = await create_table_record(
        Realm,
        db,
        {
            "slug": slug,
            "name": name,
            "issuer_path": issuer_path,
            "description": payload.description,
        },
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
    await _require_superuser(request, db)
    row = await read_table_record(Realm, db, _uuid(realm_id, label="realm_id"))
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
    await _require_superuser(request, db)
    if payload is None:
        payload = AdminRealmUpdateIn.model_validate(await request.json() or {})
    row = await read_table_record(Realm, db, _uuid(realm_id, label="realm_id"))
    if row is None:
        raise HTTPException(404, "realm not found")
    changes: dict[str, Any] = {}
    next_slug = str(field_value(row, "slug"))
    if payload.slug is not None:
        next_slug = payload.slug.strip().lower()
        changes["slug"] = next_slug
    if payload.name is not None:
        changes["name"] = payload.name.strip()
    if payload.issuer_path is not None:
        changes["issuer_path"] = _issuer_path(payload.issuer_path, next_slug)
    if payload.description is not None:
        changes["description"] = payload.description
    if changes:
        row = await update_table_record(Realm, db, field_value(row, "id"), changes)
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
    await _require_superuser(request, db)
    row = await read_table_record(Realm, db, _uuid(realm_id, label="realm_id"))
    if row is None:
        raise HTTPException(404, "realm not found")
    if await list_table_records(Tenant, db, {"realm_id": field_value(row, "id")}):
        raise HTTPException(400, "cannot delete a realm that still owns tenants")
    snapshot = _realm_payload(row)
    await delete_table_record(Realm, db, field_value(row, "id"))
    return snapshot


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
    await _require_superuser(request, db)
    rows = await list_table_records(
        Tenant,
        db,
        {"realm_id": _uuid(realm_id, label="realm_id")},
    )
    rows = sorted(
        rows,
        key=lambda row: (
            field_value(row, "created_at") or "",
            field_value(row, "name", ""),
            field_value(row, "slug", ""),
        ),
    )
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
    await _require_superuser(request, db)
    if payload is None:
        payload = AdminTenantProvisionIn.model_validate(await request.json() or {})
    realm = await read_table_record(Realm, db, _uuid(realm_id, label="realm_id"))
    if realm is None:
        raise HTTPException(404, "realm not found")
    slug = payload.slug.strip().lower()
    name = payload.name.strip()
    email = payload.email.strip().lower()
    if await _find_tenant_duplicate(db, slug=slug, name=name, email=email):
        raise HTTPException(409, "tenant slug, name, or email already exists")
    row = await create_table_record(
        Tenant,
        db,
        {
            "slug": slug,
            "name": name,
            "email": email,
            "realm_id": field_value(realm, "id"),
        },
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
