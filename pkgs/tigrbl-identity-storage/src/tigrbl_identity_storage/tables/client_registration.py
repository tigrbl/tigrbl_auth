"""Durable dynamic client registration metadata."""

from __future__ import annotations

import datetime as dt
from typing import Any

from tigrbl_auth.framework import (
    Base,
    TenantColumn,
    Timestamped,
    S,
    acol,
    JSON,
    Mapped,
    String,
    TZDateTime,
    GUIDPk,
    ForeignKeySpec,
    PgUUID,
    UUID,
)


class ClientRegistration(Base, GUIDPk, Timestamped, TenantColumn):
    __tablename__ = "client_registrations"
    __table_args__ = ({"schema": "authn"},)

    client_id: Mapped[UUID] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.clients.id"), nullable=False, unique=True, index=True)
    )
    software_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    software_version: Mapped[str | None] = acol(storage=S(String(128), nullable=True))
    contacts: Mapped[list[str] | None] = acol(storage=S(JSON, nullable=True))
    registration_metadata: Mapped[dict[str, Any] | None] = acol(storage=S(JSON, nullable=True))
    registration_access_token_hash: Mapped[str | None] = acol(
        storage=S(String(128), nullable=True, unique=True, index=True)
    )
    registration_client_uri: Mapped[str | None] = acol(storage=S(String(1000), nullable=True))
    issued_at: Mapped[dt.datetime] = acol(
        storage=S(TZDateTime, nullable=False, default=lambda: dt.datetime.now(dt.timezone.utc))
    )
    rotated_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True))
    disabled_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))


__all__ = ["ClientRegistration"]
