"""Durable dynamic client registration metadata."""

from __future__ import annotations

import datetime as dt
from typing import Any

from tigrbl_identity_server.framework import (
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
from ._ops import create_record, delete_record, first_record, record_id, update_record, utc_now


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

    @classmethod
    async def register_client(cls, db: Any, **payload: Any) -> "ClientRegistration":
        payload.setdefault("issued_at", utc_now())
        return await create_record(cls, db, payload)

    @classmethod
    async def read_registration(cls, db: Any, *, client_id: UUID) -> "ClientRegistration | None":
        return await first_record(cls, db, {"client_id": client_id})

    @classmethod
    async def update_registration(cls, db: Any, *, client_id: UUID, **payload: Any) -> "ClientRegistration | None":
        row = await cls.read_registration(db, client_id=client_id)
        if row is None:
            return None
        return await update_record(cls, db, record_id(row), payload)

    @classmethod
    async def delete_registration(cls, db: Any, *, client_id: UUID) -> Any:
        row = await cls.read_registration(db, client_id=client_id)
        if row is None:
            return None
        return await delete_record(cls, db, record_id(row))


__all__ = ["ClientRegistration"]
