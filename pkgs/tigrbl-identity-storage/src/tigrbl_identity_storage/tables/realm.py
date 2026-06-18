"""Realm model for issuer and namespace boundaries."""

from __future__ import annotations

import uuid
from typing import Any

from tigrbl_identity_server.framework import (
    Base,
    Bootstrappable,
    BaseModel,
    ColumnSpec,
    F,
    GUIDPk,
    IO,
    Mapped,
    S,
    String,
    Timestamped,
    acol,
    relationship,
    constr,
)
from ._ops import create_record, first_record, list_records, record_id, update_record

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


__all__ = [
    "AdminRealmOut",
    "AdminRealmProvisionIn",
    "AdminRealmUpdateIn",
    "Realm",
]
