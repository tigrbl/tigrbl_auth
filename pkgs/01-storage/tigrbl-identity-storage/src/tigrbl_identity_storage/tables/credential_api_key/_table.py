"""Durable API-key credential records."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from tigrbl_identity_storage.framework import (
    Created,
    ColumnSpec,
    F,
    GUIDPk,
    IO,
    KeyDigest,
    LastUsed,
    ValidityWindow,
    RestOltpTable,
    S,
    acol,
    Mapped,
    String,
)
from .._ops import first_record


class CredentialApiKey(RestOltpTable, GUIDPk, Created, LastUsed, ValidityWindow, KeyDigest):
    __tablename__ = "credential_api_keys"
    __table_args__ = {"extend_existing": True, "schema": "authn"}

    label: Mapped[str] = acol(
        spec=ColumnSpec(
            storage=S(String, nullable=False),
            field=F(constraints={"max_length": 120}, required_in=("create",)),
            io=IO(in_verbs=("create",), out_verbs=("read", "list"), filter_ops=("eq",)),
        )
    )
    principal_id: Mapped[str] = acol(
        spec=ColumnSpec(
            storage=S(String(255), nullable=False, index=True),
            field=F(constraints={"max_length": 255}, required_in=("create",)),
            io=IO(in_verbs=("create",), out_verbs=("read", "list"), filter_ops=("eq",)),
        )
    )
    principal_kind: Mapped[str] = acol(
        spec=ColumnSpec(
            storage=S(String(64), nullable=False, default="user", index=True),
            field=F(constraints={"max_length": 64}, required_in=("create",)),
            io=IO(in_verbs=("create",), out_verbs=("read", "list"), filter_ops=("eq",)),
        )
    )

    @classmethod
    async def lookup_active(cls, db: Any, *, digest: str) -> "CredentialApiKey | None":
        row = await first_record(cls, db, {"digest": digest})
        if row is None:
            return None
        now = datetime.now(timezone.utc)
        valid_from = getattr(row, "valid_from", None)
        valid_to = getattr(row, "valid_to", None)
        if isinstance(valid_from, datetime) and (valid_from if valid_from.tzinfo else valid_from.replace(tzinfo=timezone.utc)) > now:
            return None
        if isinstance(valid_to, datetime) and (valid_to if valid_to.tzinfo else valid_to.replace(tzinfo=timezone.utc)) <= now:
            return None
        return row


__all__ = ["CredentialApiKey"]
