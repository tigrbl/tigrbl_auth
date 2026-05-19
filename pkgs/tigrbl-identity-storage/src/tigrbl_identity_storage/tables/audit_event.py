"""Durable audit events for operator and protocol actions."""

from __future__ import annotations

import datetime as dt
import uuid

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
)


class AuditEvent(Base, GUIDPk, Timestamped, TenantColumn):
    __tablename__ = "audit_events"
    __table_args__ = ({"schema": "authn"},)

    actor_user_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.users.id"), nullable=True, index=True)
    )
    actor_client_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.clients.id"), nullable=True, index=True)
    )
    session_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.sessions.id"), nullable=True, index=True)
    )
    event_type: Mapped[str] = acol(storage=S(String(128), nullable=False, index=True))
    target_type: Mapped[str | None] = acol(storage=S(String(64), nullable=True))
    target_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    outcome: Mapped[str] = acol(storage=S(String(32), nullable=False, default="success"))
    request_id: Mapped[str | None] = acol(storage=S(String(128), nullable=True, index=True))
    details: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    occurred_at: Mapped[dt.datetime] = acol(
        storage=S(TZDateTime, nullable=False, default=lambda: dt.datetime.now(dt.timezone.utc))
    )


__all__ = ["AuditEvent"]
