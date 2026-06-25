"""Tenant model for the authentication service."""

from __future__ import annotations

import uuid

from tigrbl_identity_storage.framework import (
    BaseModel,
    Bootstrappable,
    F,
    IO,
    S,
    ColumnSpec,
    ForeignKeySpec,
    Mapped,
    PgUUID,
    String,
    TenantBase,
    acol,
    constr,
    relationship,
)

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


__all__ = [
    "AdminTenantOut",
    "AdminTenantProvisionIn",
    "AdminTenantUpdateIn",
    "Tenant",
]
