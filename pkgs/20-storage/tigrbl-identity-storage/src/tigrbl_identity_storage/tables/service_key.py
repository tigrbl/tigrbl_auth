"""Service key model for the authentication service."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from tigrbl_identity_storage.framework import (
    ForeignKeySpec,
    Created,
    GUIDPk,
    KeyDigest,
    LastUsed,
    ValidityWindow,
    RestOltpTable,
    F,
    IO,
    S,
    acol,
    Mapped,
    PgUUID,
    String,
    relationship,
)
from ._ops import first_record


class ServiceKey(RestOltpTable, GUIDPk, Created, LastUsed, ValidityWindow, KeyDigest):
    __tablename__ = "service_keys"
    __table_args__ = {"extend_existing": True, "schema": "authn"}

    label: Mapped[str] = acol(
        storage=S(String, nullable=False),
        field=F(constraints={"max_length": 120}, required_in=("create",)),
        io=IO(in_verbs=("create",), out_verbs=("read", "list"), filter_ops=("eq",)),
    )
    service_id: Mapped[UUID] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.services.id"), index=True, nullable=False),
        field=F(py_type=UUID, required_in=("create",)),
        io=IO(in_verbs=("create",), out_verbs=("read", "list"), filter_ops=("eq",)),
    )

    _service = relationship("Service", back_populates="_service_keys", lazy="joined")

    @classmethod
    async def lookup_active(cls, db: Any, *, digest: str) -> "ServiceKey | None":
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


__all__ = ["ServiceKey"]
