"""User model for the authentication service."""

from __future__ import annotations

import uuid
import datetime as dt

from tigrbl_identity_storage.framework import (
    UserBase,
    LargeBinary,
    Mapped,
    Boolean,
    String,
    TZDateTime,
    relationship,
    F,
    IO,
    S,
    acol,
    ColumnSpec,
)

DEFAULT_BOOTSTRAP_SUPERUSER_ID = uuid.UUID("FFFFFFFF-0000-0000-0000-000000000001")


class User(UserBase):
    __table_args__ = ({"extend_existing": True, "schema": "authn"},)

    username: Mapped[str] = acol(
        spec=ColumnSpec(
            storage=S(String(32), nullable=False),
            field=F(constraints={"max_length": 32}, required_in=("create",)),
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
    password_hash: Mapped[bytes | None] = acol(
        spec=ColumnSpec(
            storage=S(LargeBinary(60)), io=IO(in_verbs=("create", "update", "replace"))
        )
    )
    is_admin: Mapped[bool] = acol(
        spec=ColumnSpec(
            storage=S(Boolean, nullable=False, default=False),
            field=F(),
            io=IO(
                in_verbs=("create", "update", "replace"),
                out_verbs=("read", "list"),
                filter_ops=("eq",),
            ),
        )
    )
    is_superuser: Mapped[bool] = acol(
        spec=ColumnSpec(
            storage=S(Boolean, nullable=False, default=False),
            field=F(),
            io=IO(
                in_verbs=("create", "update", "replace"),
                out_verbs=("read", "list"),
                filter_ops=("eq",),
            ),
        )
    )
    must_change_password: Mapped[bool] = acol(
        spec=ColumnSpec(
            storage=S(Boolean, nullable=False, default=False),
            field=F(),
            io=IO(
                in_verbs=("create", "update", "replace"),
                out_verbs=("read", "list"),
                filter_ops=("eq",),
            ),
        )
    )
    password_reset_token_hash: Mapped[str | None] = acol(
        spec=ColumnSpec(
            storage=S(String(128), nullable=True, index=True),
            io=IO(in_verbs=("update", "replace")),
        )
    )
    password_reset_expires_at: Mapped[dt.datetime | None] = acol(
        spec=ColumnSpec(
            storage=S(TZDateTime, nullable=True),
            io=IO(in_verbs=("update", "replace"), out_verbs=("read",)),
        )
    )

    tenant = relationship("Tenant", back_populates="users")

    @property
    def roles(self) -> tuple[str, ...]:
        roles: list[str] = []
        if self.is_admin:
            roles.append("admin")
        if self.is_superuser:
            roles.append("superuser")
        return tuple(roles)

    @property
    def scopes(self) -> tuple[str, ...]:
        scopes: list[str] = []
        if self.is_admin:
            scopes.append("tigrbl_auth:admin")
        if self.is_superuser:
            scopes.append("tigrbl_auth:superuser")
        return tuple(scopes)

__all__ = [
    "DEFAULT_BOOTSTRAP_SUPERUSER_ID",
    "User",
]
