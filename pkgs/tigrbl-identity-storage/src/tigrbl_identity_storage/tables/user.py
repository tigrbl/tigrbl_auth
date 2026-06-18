"""User model for the authentication service."""

from __future__ import annotations

import uuid
import datetime as dt
from typing import Any

from tigrbl_identity_server.framework import (
    UserBase,
    Bootstrappable,
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

from tigrbl_identity_jose.key_management import hash_pw
from ._ops import create_record, first_record, list_records, record_id, update_record

DEFAULT_BOOTSTRAP_SUPERUSER_ID = uuid.UUID("FFFFFFFF-0000-0000-0000-000000000001")
DEFAULT_BOOTSTRAP_SUPERUSER_PASSWORD = "AdminPass123!"


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
        spec=ColumnSpec(storage=S(LargeBinary(60)), io=IO(in_verbs=("create", "update", "replace")))
    )
    is_admin: Mapped[bool] = acol(
        spec=ColumnSpec(
            storage=S(Boolean, nullable=False, default=False),
            field=F(),
            io=IO(in_verbs=("create", "update", "replace"), out_verbs=("read", "list"), filter_ops=("eq",)),
        )
    )
    is_superuser: Mapped[bool] = acol(
        spec=ColumnSpec(
            storage=S(Boolean, nullable=False, default=False),
            field=F(),
            io=IO(in_verbs=("create", "update", "replace"), out_verbs=("read", "list"), filter_ops=("eq",)),
        )
    )
    must_change_password: Mapped[bool] = acol(
        spec=ColumnSpec(
            storage=S(Boolean, nullable=False, default=False),
            field=F(),
            io=IO(in_verbs=("create", "update", "replace"), out_verbs=("read", "list"), filter_ops=("eq",)),
        )
    )
    password_reset_token_hash: Mapped[str | None] = acol(
        spec=ColumnSpec(storage=S(String(128), nullable=True, index=True), io=IO(in_verbs=("update", "replace")))
    )
    password_reset_expires_at: Mapped[dt.datetime | None] = acol(
        spec=ColumnSpec(storage=S(TZDateTime, nullable=True), io=IO(in_verbs=("update", "replace"), out_verbs=("read",)))
    )

    _api_keys = relationship("ApiKey", back_populates="_user", cascade="all, delete-orphan")
    tenant = relationship("Tenant", back_populates="users")

    @classmethod
    def new(cls, *, tenant_id: uuid.UUID, username: str, email: str, password: str):
        return cls(
            tenant_id=tenant_id,
            username=username,
            email=email,
            password_hash=hash_pw(password) if password is not None else None,
        )

    @classmethod
    async def create_user(cls, db: Any, **payload: Any) -> "User":
        if "password" in payload and "password_hash" not in payload:
            payload["password_hash"] = hash_pw(str(payload.pop("password")))
        return await create_record(cls, db, payload)

    @classmethod
    async def update_user(cls, db: Any, *, user_id: uuid.UUID, **payload: Any) -> "User | None":
        if "password" in payload and "password_hash" not in payload:
            payload["password_hash"] = hash_pw(str(payload.pop("password")))
        row = await first_record(cls, db, {"id": user_id})
        if row is None:
            return None
        return await update_record(cls, db, record_id(row), payload)

    @classmethod
    async def disable_user(cls, db: Any, *, user_id: uuid.UUID) -> "User | None":
        return await cls.update_user(db, user_id=user_id, is_active=False)

    @classmethod
    async def list_by_tenant(cls, db: Any, *, tenant_id: uuid.UUID) -> list["User"]:
        return await list_records(cls, db, {"tenant_id": tenant_id})

    @classmethod
    async def lookup_by_identifier(cls, db: Any, *, identifier: str) -> "User | None":
        for row in await list_records(cls, db, {"username": identifier}):
            if getattr(row, "is_active", True):
                return row
        for row in await list_records(cls, db, {"email": identifier}):
            if getattr(row, "is_active", True):
                return row
        return None

    def verify_password(self, plain: str) -> bool:
        from tigrbl_identity_jose.key_management import verify_pw
        if self.password_hash is None:
            return False
        return verify_pw(plain, self.password_hash)

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


__all__ = ["DEFAULT_BOOTSTRAP_SUPERUSER_ID", "DEFAULT_BOOTSTRAP_SUPERUSER_PASSWORD", "User"]
