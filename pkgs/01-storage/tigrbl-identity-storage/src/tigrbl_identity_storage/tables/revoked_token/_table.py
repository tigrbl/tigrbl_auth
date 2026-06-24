"""Durable revoked token registry."""

from __future__ import annotations

import datetime as dt
import uuid

from tigrbl_identity_storage.framework import (
    RestOltpTable,
    BaseModel,
    Timestamped,
    S,
    acol,
    Mapped,
    String,
    GUIDPk,
    TZDateTime,
    PgUUID,
    ForeignKeySpec,
)


class RevocationIn(BaseModel):
    token: str
    token_type_hint: str | None = None


class RevocationOut(BaseModel):
    revoked: bool = True


class RevokedToken(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "revoked_tokens"
    __table_args__ = ({"schema": "authn"},)

    token_hash: Mapped[str] = acol(storage=S(String(128), nullable=False, unique=True, index=True, default=lambda: uuid.uuid4().hex))
    token_type_hint: Mapped[str | None] = acol(storage=S(String(64), nullable=True))
    refresh_family_id: Mapped[str | None] = acol(storage=S(String(64), nullable=True, index=True))
    subject: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    tenant_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.tenants.id"), nullable=True, index=True)
    )
    client_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.clients.id"), nullable=True, index=True)
    )
    revoked_reason: Mapped[str | None] = acol(storage=S(String(128), nullable=True))
    expires_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))


__all__ = ["RevocationIn", "RevocationOut", "RevokedToken"]
