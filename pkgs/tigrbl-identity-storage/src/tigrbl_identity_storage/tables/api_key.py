"""API key model for the authentication service."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from tigrbl_identity_server.framework import (
    Created,
    GUIDPk,
    KeyDigest,
    LastUsed,
    UserColumn,
    ValidityWindow,
    Base,
    F,
    S,
    acol,
    Mapped,
    String,
    relationship,
)
from ._ops import first_record


class ApiKey(Base, GUIDPk, Created, LastUsed, ValidityWindow, UserColumn, KeyDigest):
    __tablename__ = "api_keys"
    __table_args__ = {"extend_existing": True, "schema": "authn"}

    label: Mapped[str] = acol(
        storage=S(String, nullable=False),
        field=F(constraints={"max_length": 120}),
    )

    _user = relationship("User", back_populates="_api_keys", lazy="joined")

    @classmethod
    async def lookup_active(cls, db: Any, *, digest: str) -> "ApiKey | None":
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


__all__ = ["ApiKey"]
