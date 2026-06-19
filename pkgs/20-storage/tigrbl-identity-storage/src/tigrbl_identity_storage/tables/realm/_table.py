"""Realm model for issuer and namespace boundaries."""

from __future__ import annotations

import uuid
from typing import Any

from tigrbl_identity_server.framework import (
    Base,
    Bootstrappable,
    BaseModel,
    ColumnSpec,
    Depends,
    F,
    GUIDPk,
    HTTPException,
    IO,
    Mapped,
    Request,
    S,
    String,
    Timestamped,
    TigrblRouter,
    acol,
    relationship,
    constr,
    status,
)
from .._ops import create_record, delete_record, first_record, list_records, read_record, record_id, update_record
from ..engine import get_db
from ..tenant import AdminTenantOut, AdminTenantProvisionIn, Tenant, _tenant_payload

_realm_description = constr(strip_whitespace=True, max_length=255)
_realm_issuer_path = constr(strip_whitespace=True, max_length=255)
_realm_name = constr(strip_whitespace=True, min_length=1, max_length=120)
_realm_slug = constr(strip_whitespace=True, min_length=3, max_length=120)


class AdminRealmOut(BaseModel):
    id: str
    slug: str
    name: str
    issuer_path: str = ""
    description: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class AdminRealmProvisionIn(BaseModel):
    slug: _realm_slug
    name: _realm_name
    issuer_path: _realm_issuer_path | None = None
    description: _realm_description | None = None


class AdminRealmUpdateIn(BaseModel):
    slug: _realm_slug | None = None
    name: _realm_name | None = None
    issuer_path: _realm_issuer_path | None = None
    description: _realm_description | None = None


class Realm(Base, GUIDPk, Timestamped, Bootstrappable):
    __tablename__ = "realms"
    __table_args__ = ({"schema": "authn"},)

    slug: Mapped[str] = acol(
        spec=ColumnSpec(
            storage=S(String(120), nullable=False, unique=True, index=True),
            field=F(constraints={"max_length": 120}, required_in=("create",)),
            io=IO(
                in_verbs=("create", "update", "replace"),
                out_verbs=("read", "list"),
                filter_ops=("eq", "ilike"),
                sortable=True,
            ),
        )
    )
    name: Mapped[str] = acol(
        spec=ColumnSpec(
            storage=S(String(120), nullable=False, unique=True),
            field=F(constraints={"max_length": 120}, required_in=("create",)),
            io=IO(
                in_verbs=("create", "update", "replace"),
                out_verbs=("read", "list"),
                filter_ops=("eq", "ilike"),
                sortable=True,
            ),
        )
    )
    issuer_path: Mapped[str] = acol(
        spec=ColumnSpec(
            storage=S(String(255), nullable=False, unique=True),
            field=F(constraints={"max_length": 255}, required_in=("create",)),
            io=IO(
                in_verbs=("create", "update", "replace"),
                out_verbs=("read", "list"),
                filter_ops=("eq", "ilike"),
                sortable=True,
            ),
        )
    )
    description: Mapped[str | None] = acol(
        spec=ColumnSpec(
            storage=S(String(255), nullable=True),
            field=F(constraints={"max_length": 255}),
            io=IO(in_verbs=("create", "update", "replace"), out_verbs=("read", "list")),
        )
    )

    tenants = relationship("Tenant", back_populates="realm")

    DEFAULT_ROWS = [
        {
            "id": uuid.UUID("FFFFFFFF-1000-0000-0000-000000000000"),
            "slug": "default",
            "name": "Default",
            "issuer_path": "",
            "description": "Default compatibility realm",
        }
    ]

    @classmethod
    async def create_realm(cls, db: Any, **payload: Any) -> "Realm":
        return await create_record(cls, db, payload)

    @classmethod
    async def update_realm(cls, db: Any, *, realm_id: uuid.UUID, **payload: Any) -> "Realm | None":
        row = await first_record(cls, db, {"id": realm_id})
        if row is None:
            return None
        return await update_record(cls, db, record_id(row), payload)

    @classmethod
    async def list_realms(cls, db: Any, **filters: Any) -> list["Realm"]:
        return await list_records(cls, db, filters)

    @classmethod
    async def lookup_by_slug(cls, db: Any, *, slug: str) -> "Realm | None":
        return await first_record(cls, db, {"slug": slug})


admin_api = admin_router = TigrblRouter()


def _realm_payload(row: Realm) -> AdminRealmOut:
    return AdminRealmOut(
        id=str(row.id),
        slug=row.slug,
        name=row.name,
        issuer_path=row.issuer_path,
        description=row.description,
        created_at=getattr(row, "created_at", None).isoformat()
        if getattr(row, "created_at", None)
        else None,
        updated_at=getattr(row, "updated_at", None).isoformat()
        if getattr(row, "updated_at", None)
        else None,
    )


async def _require_superuser(request: Request, db: Any) -> Any:
    from tigrbl_identity_admin.bootstrap import resolve_admin_user_from_request

    actor = await resolve_admin_user_from_request(request, db=db)
    if actor is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "authenticated admin session required")
    if not bool(getattr(actor, "is_superuser", False)):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "superuser privileges required")
    return actor


def _uuid(value: str, *, label: str) -> uuid.UUID:
    try:
        return uuid.UUID(str(value))
    except Exception as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"invalid {label}") from exc


def _issuer_path(value: str | None, slug: str) -> str:
    text = (value if value is not None else f"/realms/{slug}").strip()
    if text == "":
        return ""
    if not text.startswith("/"):
        text = f"/{text}"
    return text.rstrip("/")


async def _find_realm_duplicate(db: Any, *, slug: str, name: str, issuer_path: str) -> Realm | None:
    for filters in ({"slug": slug}, {"name": name}, {"issuer_path": issuer_path}):
        row = await first_record(Realm, db, filters)
        if row is not None:
            return row
    return None


async def _find_tenant_duplicate(db: Any, *, slug: str, name: str, email: str) -> Tenant | None:
    for filters in ({"slug": slug}, {"name": name}, {"email": email}):
        row = await first_record(Tenant, db, filters)
        if row is not None:
            return row
    return None


@admin_api.route("/admin/realm", methods=["GET"], response_model=list[AdminRealmOut])
async def admin_list_realms(
    request: Request,
    db: Any = Depends(get_db),
) -> list[AdminRealmOut]:
    await _require_superuser(request, db)
    rows = await list_records(Realm, db)
    rows = sorted(
        rows,
        key=lambda row: (
            getattr(row, "created_at", None) or "",
            getattr(row, "name", ""),
            getattr(row, "slug", ""),
        ),
    )
    return [_realm_payload(row) for row in rows]


@admin_api.route("/admin/realm", methods=["POST"], response_model=AdminRealmOut)
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
    existing = await _find_realm_duplicate(db, slug=slug, name=name, issuer_path=issuer_path)
    if existing is not None:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "realm slug, name, or issuer path already exists",
        )
    row = await create_record(
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


@admin_api.route("/admin/realm/{realm_id}", methods=["GET"], response_model=AdminRealmOut)
async def admin_get_realm(
    request: Request,
    realm_id: str,
    db: Any = Depends(get_db),
) -> AdminRealmOut:
    await _require_superuser(request, db)
    row = await read_record(Realm, db, _uuid(realm_id, label="realm_id"))
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "realm not found")
    return _realm_payload(row)


@admin_api.route("/admin/realm/{realm_id}", methods=["PATCH"], response_model=AdminRealmOut)
async def admin_update_realm(
    request: Request,
    realm_id: str,
    payload: AdminRealmUpdateIn | None = None,
    db: Any = Depends(get_db),
) -> AdminRealmOut:
    await _require_superuser(request, db)
    if payload is None:
        payload = AdminRealmUpdateIn.model_validate(await request.json() or {})
    row = await read_record(Realm, db, _uuid(realm_id, label="realm_id"))
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "realm not found")
    changes: dict[str, Any] = {}
    next_slug = row.slug
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
        row = await update_record(Realm, db, row.id, changes)
    return _realm_payload(row)


@admin_api.route("/admin/realm/{realm_id}", methods=["DELETE"], response_model=AdminRealmOut)
async def admin_delete_realm(
    request: Request,
    realm_id: str,
    db: Any = Depends(get_db),
) -> AdminRealmOut:
    await _require_superuser(request, db)
    row = await read_record(Realm, db, _uuid(realm_id, label="realm_id"))
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "realm not found")
    tenant_count = len(await list_records(Tenant, db, {"realm_id": row.id}))
    if tenant_count:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "cannot delete a realm that still owns tenants",
        )
    snapshot = _realm_payload(row)
    await delete_record(Realm, db, row.id)
    return snapshot


@admin_api.route(
    "/admin/realm/{realm_id}/tenant",
    methods=["GET"],
    response_model=list[AdminTenantOut],
)
async def admin_list_realm_tenants(
    request: Request,
    realm_id: str,
    db: Any = Depends(get_db),
) -> list[AdminTenantOut]:
    await _require_superuser(request, db)
    rid = _uuid(realm_id, label="realm_id")
    rows = await list_records(Tenant, db, {"realm_id": rid})
    rows = sorted(
        rows,
        key=lambda row: (
            getattr(row, "created_at", None) or "",
            getattr(row, "name", ""),
            getattr(row, "slug", ""),
        ),
    )
    return [_tenant_payload(row) for row in rows]


@admin_api.route(
    "/admin/realm/{realm_id}/tenant",
    methods=["POST"],
    response_model=AdminTenantOut,
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
    realm = await read_record(Realm, db, _uuid(realm_id, label="realm_id"))
    if realm is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "realm not found")
    slug = payload.slug.strip().lower()
    name = payload.name.strip()
    email = payload.email.strip().lower()
    existing = await _find_tenant_duplicate(db, slug=slug, name=name, email=email)
    if existing is not None:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "tenant slug, name, or email already exists",
        )
    row = await create_record(
        Tenant,
        db,
        {"slug": slug, "name": name, "email": email, "realm_id": realm.id},
    )
    return _tenant_payload(row)


Realm.admin_list_realms = staticmethod(admin_list_realms)  # type: ignore[attr-defined]
Realm.admin_create_realm = staticmethod(admin_create_realm)  # type: ignore[attr-defined]
Realm.admin_get_realm = staticmethod(admin_get_realm)  # type: ignore[attr-defined]
Realm.admin_update_realm = staticmethod(admin_update_realm)  # type: ignore[attr-defined]
Realm.admin_delete_realm = staticmethod(admin_delete_realm)  # type: ignore[attr-defined]
Realm.admin_list_realm_tenants = staticmethod(admin_list_realm_tenants)  # type: ignore[attr-defined]
Realm.admin_create_realm_tenant = staticmethod(admin_create_realm_tenant)  # type: ignore[attr-defined]


__all__ = [
    "AdminRealmOut",
    "AdminRealmProvisionIn",
    "AdminRealmUpdateIn",
    "Realm",
    "admin_api",
    "admin_router",
    "admin_create_realm",
    "admin_create_realm_tenant",
    "admin_delete_realm",
    "admin_get_realm",
    "admin_list_realm_tenants",
    "admin_list_realms",
    "admin_update_realm",
]
