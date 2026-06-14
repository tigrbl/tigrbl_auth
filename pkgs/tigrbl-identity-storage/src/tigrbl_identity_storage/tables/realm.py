"""Realm model for issuer and namespace boundaries."""

from __future__ import annotations

import uuid

from tigrbl_identity_server.framework import (
    Base,
    Bootstrappable,
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
)


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


__all__ = ["Realm"]
