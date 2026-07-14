"""User model for the authentication service."""

from __future__ import annotations

import uuid
import datetime as dt
from typing import Any

from tigrbl_identity_storage.framework import (
    UserBase,
    Bootstrappable,
    BaseModel,
    Field,
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
    constr,
    op_ctx,
)

from tigrbl_identity_jose.key_management import hash_pw

DEFAULT_BOOTSTRAP_SUPERUSER_ID = uuid.UUID("FFFFFFFF-0000-0000-0000-000000000001")
DEFAULT_BOOTSTRAP_SUPERUSER_PASSWORD = "AdminPass123!"
_password = constr(min_length=8, max_length=256)


class CredsIn(BaseModel):
    identifier: constr(strip_whitespace=True, min_length=3, max_length=120)
    password: _password


class AdminPasswordResetRequestIn(BaseModel):
    identifier: constr(strip_whitespace=True, min_length=3, max_length=120)


class AdminPasswordResetCompleteIn(BaseModel):
    token: constr(strip_whitespace=True, min_length=16, max_length=256)
    password: _password


class AdminPasswordChangeIn(BaseModel):
    current_password: _password
    new_password: _password


class AdminSessionOut(BaseModel):
    authenticated: bool
    session_id: str | None = None
    user_id: str | None = None
    tenant_id: str | None = None
    username: str | None = None
    email: str | None = None
    is_admin: bool = False
    is_superuser: bool = False
    must_change_password: bool = False
    roles: list[str] = Field(default_factory=list)
    debug_reset_token: str | None = None


class User(UserBase, Bootstrappable):
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

    DEFAULT_ROWS = [
        {
            "id": DEFAULT_BOOTSTRAP_SUPERUSER_ID,
            "tenant_id": uuid.UUID("FFFFFFFF-0000-0000-0000-000000000000"),
            "username": "admin",
            "email": "admin@example.com",
            "password_hash": hash_pw(DEFAULT_BOOTSTRAP_SUPERUSER_PASSWORD),
            "is_admin": True,
            "is_superuser": True,
            "must_change_password": True,
            "is_active": True,
        }
    ]


@op_ctx(bind=User, alias="lookup_by_identifier", target="custom", arity="collection", rest=False)
async def lookup_by_identifier(cls: type[User], ctx: dict[str, Any]):
    from .._ops import field, list_records

    identifier = str((ctx.get("payload") or {}).get("identifier") or "")
    if not identifier:
        return None
    for row in await list_records(cls, ctx["db"]):
        if not bool(field(row, "is_active", True)):
            continue
        if identifier in {field(row, "username"), field(row, "email")}:
            return row
    return None


ADMIN_AUTH_TAGS = ["Admin Auth"]


__all__ = [
    "AdminPasswordChangeIn",
    "AdminPasswordResetCompleteIn",
    "AdminPasswordResetRequestIn",
    "AdminSessionOut",
    "CredsIn",
    "DEFAULT_BOOTSTRAP_SUPERUSER_ID",
    "DEFAULT_BOOTSTRAP_SUPERUSER_PASSWORD",
    "User",
]
