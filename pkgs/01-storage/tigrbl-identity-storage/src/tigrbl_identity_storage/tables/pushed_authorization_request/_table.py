"""Pushed authorization request model with durable lifecycle fields."""

from __future__ import annotations

import datetime as dt
import uuid
from datetime import datetime, timedelta, timezone

from tigrbl_identity_storage.framework import (
    RestOltpTable,
    Timestamped,
    S,
    acol,
    JSON,
    Mapped,
    String,
    Integer,
    TZDateTime,
    GUIDPk,
    ForeignKeySpec,
    PgUUID,
)

DEFAULT_PAR_EXPIRY = 90


def _default_request_uri() -> str:
    return f"urn:ietf:params:oauth:request_uri:{uuid.uuid4()}"


def _default_expires_in() -> int:
    return DEFAULT_PAR_EXPIRY


def _default_expires_at() -> datetime:
    return datetime.now(tz=timezone.utc) + timedelta(seconds=_default_expires_in())


class PushedAuthorizationRequest(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "par_requests"
    __table_args__ = ({"schema": "authn"},)

    request_uri: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, default=_default_request_uri))
    client_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.clients.id"), nullable=True, index=True)
    )
    tenant_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.tenants.id"), nullable=True, index=True)
    )
    params: Mapped[dict] = acol(storage=S(JSON, nullable=False, default=dict))
    expires_in: Mapped[int] = acol(storage=S(Integer, nullable=False, default=_default_expires_in))
    expires_at: Mapped[dt.datetime] = acol(storage=S(TZDateTime, nullable=False, default=_default_expires_at))
    consumed_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))


__all__ = [
    "DEFAULT_PAR_EXPIRY",
    "PushedAuthorizationRequest",
]
