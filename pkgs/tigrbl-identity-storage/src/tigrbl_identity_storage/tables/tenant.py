"""Tenant model for the authentication service."""

from __future__ import annotations

import uuid
from typing import Any

from tigrbl_identity_server.framework import (
    TenantBase,
    Bootstrappable,
    BaseModel,
    F,
    IO,
    S,
    acol,
    ColumnSpec,
    Mapped,
    String,
    PgUUID,
    ForeignKeySpec,
    relationship,
    constr,
)
from ._ops import create_record, first_record, list_records, record_id, update_record

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
    async def create_tenant(cls, db: Any, **payload: Any) -> "Tenant":
        return await create_record(cls, db, payload)

    @classmethod
    async def update_tenant(cls, db: Any, *, tenant_id: uuid.UUID, **payload: Any) -> "Tenant | None":
        row = await first_record(cls, db, {"id": tenant_id})
        if row is None:
            return None
        return await update_record(cls, db, record_id(row), payload)

    @classmethod
    async def disable_tenant(cls, db: Any, *, tenant_id: uuid.UUID) -> "Tenant | None":
        return await cls.update_tenant(db, tenant_id=tenant_id, is_active=False)

    @classmethod
    async def list_by_realm(cls, db: Any, *, realm_id: uuid.UUID | None) -> list["Tenant"]:
        return await list_records(cls, db, {"realm_id": realm_id})

    @classmethod
    async def lookup_by_name(cls, db: Any, *, name: str) -> "Tenant | None":
        return await first_record(cls, db, {"name": name})


__all__ = [
    "AdminTenantOut",
    "AdminTenantProvisionIn",
    "AdminTenantUpdateIn",
    "Tenant",
]
