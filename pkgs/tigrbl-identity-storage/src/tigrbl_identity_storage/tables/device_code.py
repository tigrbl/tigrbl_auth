"""Device code model with durable authorization lifecycle fields."""

from __future__ import annotations

import datetime as dt
import uuid

from tigrbl_auth.framework import (
    Base,
    Timestamped,
    S,
    acol,
    ForeignKeySpec,
    Boolean,
    Integer,
    Mapped,
    PgUUID,
    String,
    TZDateTime,
    GUIDPk,
)


class DeviceCode(Base, GUIDPk, Timestamped):
    __tablename__ = "device_codes"
    __table_args__ = ({"schema": "authn"},)

    device_code: Mapped[str] = acol(storage=S(String(128), nullable=False, unique=True))
    user_code: Mapped[str] = acol(storage=S(String(32), nullable=False, index=True))
    client_id: Mapped[uuid.UUID] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.clients.id"), nullable=False)
    )
    scope: Mapped[str | None] = acol(storage=S(String(1000), nullable=True))
    audience: Mapped[str | None] = acol(storage=S(String(1000), nullable=True))
    resource: Mapped[str | None] = acol(storage=S(String(1000), nullable=True))
    expires_at: Mapped[dt.datetime] = acol(storage=S(TZDateTime, nullable=False))
    interval: Mapped[int] = acol(storage=S(Integer, nullable=False))
    poll_count: Mapped[int] = acol(storage=S(Integer, nullable=False, default=0))
    slow_down_count: Mapped[int] = acol(storage=S(Integer, nullable=False, default=0))
    last_polled_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    authorized: Mapped[bool] = acol(storage=S(Boolean, nullable=False, default=False))
    authorized_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    denied_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    denial_reason: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    consumed_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    user_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.users.id"), nullable=True, index=True)
    )
    tenant_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.tenants.id"), nullable=True, index=True)
    )


__all__ = ["DeviceCode"]
