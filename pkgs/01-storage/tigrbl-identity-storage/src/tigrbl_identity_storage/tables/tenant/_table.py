"""Tenant model for the authentication service."""

from __future__ import annotations

import uuid

from tigrbl_identity_storage.framework import (
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
    relationship,
)


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


__all__ = ["Tenant"]
