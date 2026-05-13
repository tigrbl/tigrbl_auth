"""Durable token status and introspection backing store."""

from __future__ import annotations

import datetime as dt
import uuid

from tigrbl_auth.framework import (
    Base,
    Timestamped,
    S,
    acol,
    JSON,
    Boolean,
    Mapped,
    String,
    TZDateTime,
    GUIDPk,
    ForeignKeySpec,
    PgUUID,
)


class TokenRecord(Base, GUIDPk, Timestamped):
    __tablename__ = "token_records"
    __table_args__ = ({"schema": "authn"},)

    token_hash: Mapped[str] = acol(storage=S(String(128), nullable=False, unique=True, index=True, default=lambda: uuid.uuid4().hex))
    token_kind: Mapped[str] = acol(storage=S(String(32), nullable=False, default="access"))
    token_type_hint: Mapped[str | None] = acol(storage=S(String(64), nullable=True))
    refresh_family_id: Mapped[str | None] = acol(storage=S(String(64), nullable=True, index=True))
    refresh_parent_hash: Mapped[str | None] = acol(storage=S(String(128), nullable=True, index=True))
    refresh_successor_hash: Mapped[str | None] = acol(storage=S(String(128), nullable=True, index=True))
    active: Mapped[bool] = acol(storage=S(Boolean, nullable=False, default=True))
    subject: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True, default="admin-created-token-record"))
    tenant_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.tenants.id"), nullable=True, index=True)
    )
    client_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.clients.id"), nullable=True, index=True)
    )
    scope: Mapped[str | None] = acol(storage=S(String(1000), nullable=True))
    issuer: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    audience: Mapped[dict | list | str | None] = acol(storage=S(JSON, nullable=True))
    claims: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    issued_at: Mapped[dt.datetime] = acol(
        storage=S(TZDateTime, nullable=False, default=lambda: dt.datetime.now(dt.timezone.utc))
    )
    expires_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    last_introspected_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True))
    used_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    reuse_detected_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    revoked_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    revoked_reason: Mapped[str | None] = acol(storage=S(String(128), nullable=True))


__all__ = ["TokenRecord"]
