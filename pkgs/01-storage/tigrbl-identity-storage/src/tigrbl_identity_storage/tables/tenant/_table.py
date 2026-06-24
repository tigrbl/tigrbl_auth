"""Tenant model for the authentication service."""

from __future__ import annotations

import uuid
from typing import Any

from tigrbl_identity_storage.framework import (
    TenantBase,
    Bootstrappable,
    BaseModel,
    Depends,
    F,
    HTTPException,
    IO,
    S,
    acol,
    ColumnSpec,
    Mapped,
    Request,
    String,
    PgUUID,
    ForeignKeySpec,
    TigrblRouter,
    relationship,
    constr,
    status,
)
from .._ops import create_record, delete_record, first_record, list_records, read_record, record_id, update_record
from ..engine import get_db

_email = constr(strip_whitespace=True, min_length=3, max_length=120)
_tenant_name = constr(strip_whitespace=True, min_length=1, max_length=120)
_tenant_slug = constr(strip_whitespace=True, min_length=3, max_length=120)


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
    slug: _tenant_slug
    name: _tenant_name
    email: _email


class AdminTenantUpdateIn(BaseModel):
    realm_id: str | None = None
    slug: _tenant_slug | None = None
    name: _tenant_name | None = None
    email: _email | None = None
    is_active: bool | None = None


class Tenant(TenantBase, Bootstrappable):
    __table_args__ = ({"extend_existing": True, "schema": "authn"},)

    name: Mapped[str] = acol(
        spec=ColumnSpec(
            storage=S(String, nullable=False, unique=True),
            field=F(constraints={"max_length": 120}, required_in=("create",)),
            io=IO(
                in_verbs=("create", "update", "replace"),
                out_verbs=("read", "list"),
                filter_ops=("eq", "ilike"),
                sortable=True,
            ),
        )
    )
    email: Mapped[str] = acol(
        spec=ColumnSpec(
            storage=S(String, nullable=False, unique=True),
            field=F(constraints={"max_length": 120}, required_in=("create",)),
            io=IO(
                in_verbs=("create", "update", "replace"),
                out_verbs=("read", "list"),
                filter_ops=("eq", "ilike"),
                sortable=True,
            ),
        )
    )
    realm_id: Mapped[uuid.UUID | None] = acol(
        spec=ColumnSpec(
            storage=S(
                PgUUID(as_uuid=True),
                fk=ForeignKeySpec(target="authn.realms.id"),
                nullable=True,
                index=True,
            ),
            field=F(),
            io=IO(
                in_verbs=("create", "update", "replace"),
                out_verbs=("read", "list"),
                filter_ops=("eq",),
                sortable=True,
            ),
        )
    )

    realm = relationship("Realm", back_populates="tenants")
    users = relationship("User", back_populates="tenant", cascade="all, delete-orphan")
    clients = relationship("Client", back_populates="tenant", cascade="all, delete-orphan")

    DEFAULT_ROWS = [
        {
            "id": uuid.UUID("FFFFFFFF-0000-0000-0000-000000000000"),
            "realm_id": uuid.UUID("FFFFFFFF-1000-0000-0000-000000000000"),
            "email": "tenant@example.com",
            "name": "Public",
            "slug": "public",
        }
    ]

    @classmethod
    async def update_tenant(cls, db: Any, *, tenant_id: uuid.UUID, **payload: Any) -> "Tenant | None":
        row = await first_record(cls, db, {"id": tenant_id})
        if row is None:
            return None
        return await update_record(cls, db, record_id(row), payload)

    @classmethod
    async def disable_tenant(cls, db: Any, *, tenant_id: uuid.UUID) -> "Tenant | None":
        return await cls.update_tenant(db, tenant_id=tenant_id, is_active=False)

admin_api = admin_router = TigrblRouter()


def _tenant_payload(row: Tenant) -> AdminTenantOut:
    return AdminTenantOut(
        id=str(row.id),
        realm_id=str(row.realm_id) if getattr(row, "realm_id", None) else None,
        slug=row.slug,
        name=row.name,
        email=row.email,
        created_at=getattr(row, "created_at", None).isoformat()
        if getattr(row, "created_at", None)
        else None,
        updated_at=getattr(row, "updated_at", None).isoformat()
        if getattr(row, "updated_at", None)
        else None,
    )


async def _require_admin(request: Request, db: Any) -> Any:
    from tigrbl_identity_admin.bootstrap import resolve_admin_user_from_request

    actor = await resolve_admin_user_from_request(request, db=db)
    if actor is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "authenticated admin session required")
    return actor


def _uuid(value: str, *, label: str) -> uuid.UUID:
    try:
        return uuid.UUID(str(value))
    except Exception as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"invalid {label}") from exc


async def _find_tenant_duplicate(db: Any, *, slug: str, name: str, email: str) -> Tenant | None:
    for filters in ({"slug": slug}, {"name": name}, {"email": email}):
        row = await first_record(Tenant, db, filters)
        if row is not None:
            return row
    return None


@admin_api.route("/admin/tenant", methods=["GET"], response_model=list[AdminTenantOut])
async def admin_list_tenants(
    request: Request,
    db: Any = Depends(get_db),
) -> list[AdminTenantOut]:
    await _require_admin(request, db)
    rows = await list_records(Tenant, db)
    rows = sorted(
        rows,
        key=lambda row: (
            getattr(row, "created_at", None) or "",
            getattr(row, "name", ""),
            getattr(row, "slug", ""),
        ),
    )
    return [_tenant_payload(row) for row in rows]


@admin_api.route("/admin/tenant", methods=["POST"], response_model=AdminTenantOut)
async def admin_create_tenant(
    request: Request,
    payload: AdminTenantProvisionIn | None = None,
    db: Any = Depends(get_db),
) -> AdminTenantOut:
    actor = await _require_admin(request, db)
    if not bool(getattr(actor, "is_superuser", False)):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "superuser privileges required to provision tenants")
    if payload is None:
        payload = AdminTenantProvisionIn.model_validate(await request.json() or {})

    slug = payload.slug.strip().lower()
    name = payload.name.strip()
    email = payload.email.strip().lower()

    existing = await _find_tenant_duplicate(db, slug=slug, name=name, email=email)
    if existing is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, "tenant slug, name, or email already exists")

    row = await create_record(
        Tenant,
        db,
        {
            "realm_id": _uuid(payload.realm_id, label="realm_id") if payload.realm_id is not None else None,
            "slug": slug,
            "name": name,
            "email": email,
        },
    )
    return _tenant_payload(row)


@admin_api.route("/admin/tenant/{tenant_id}", methods=["DELETE"], response_model=AdminTenantOut)
async def admin_delete_tenant(
    request: Request,
    tenant_id: str,
    db: Any = Depends(get_db),
) -> AdminTenantOut:
    actor = await _require_admin(request, db)
    if not bool(getattr(actor, "is_superuser", False)):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "superuser privileges required to delete tenants")

    row = await read_record(Tenant, db, _uuid(tenant_id, label="tenant_id"))
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "tenant not found")
    if row.slug == "public":
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "cannot delete the default public tenant")
    if str(actor.tenant_id) == str(row.id):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "cannot delete the current administrator tenant")

    snapshot = _tenant_payload(row)
    await delete_record(Tenant, db, row.id)
    return snapshot


@admin_api.route("/admin/tenant/{tenant_id}", methods=["PATCH"], response_model=AdminTenantOut)
async def admin_update_tenant(
    request: Request,
    tenant_id: str,
    payload: AdminTenantUpdateIn | None = None,
    db: Any = Depends(get_db),
) -> AdminTenantOut:
    actor = await _require_admin(request, db)
    if not bool(getattr(actor, "is_superuser", False)):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "superuser privileges required to update tenants")
    if payload is None:
        payload = AdminTenantUpdateIn.model_validate(await request.json() or {})

    row = await read_record(Tenant, db, _uuid(tenant_id, label="tenant_id"))
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "tenant not found")
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
        duplicate = await _find_tenant_duplicate(
            db,
            slug=changes.get("slug", row.slug),
            name=changes.get("name", row.name),
            email=changes.get("email", row.email),
        )
        if duplicate is not None and str(duplicate.id) != str(row.id):
            raise HTTPException(status.HTTP_409_CONFLICT, "tenant slug, name, or email already exists")
        row = await update_record(Tenant, db, row.id, changes)
    return _tenant_payload(row)


Tenant.admin_list_tenants = staticmethod(admin_list_tenants)  # type: ignore[attr-defined]
Tenant.admin_create_tenant = staticmethod(admin_create_tenant)  # type: ignore[attr-defined]
Tenant.admin_delete_tenant = staticmethod(admin_delete_tenant)  # type: ignore[attr-defined]
Tenant.admin_update_tenant = staticmethod(admin_update_tenant)  # type: ignore[attr-defined]


__all__ = [
    "AdminTenantOut",
    "AdminTenantProvisionIn",
    "AdminTenantUpdateIn",
    "Tenant",
    "admin_api",
    "admin_router",
    "admin_create_tenant",
    "admin_delete_tenant",
    "admin_list_tenants",
    "admin_update_tenant",
]
