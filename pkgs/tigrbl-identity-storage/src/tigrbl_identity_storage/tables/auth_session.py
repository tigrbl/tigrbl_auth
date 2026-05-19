"""Authentication session model with durable browser-session cookie state."""

from __future__ import annotations

import datetime as dt

from tigrbl_auth.framework import (
    Base,
    TenantColumn,
    Timestamped,
    UserColumn,
    S,
    acol,
    Mapped,
    String,
    TZDateTime,
    GUIDPk,
    ForeignKeySpec,
    PgUUID,
    UUID,
)


class AuthSession(Base, GUIDPk, Timestamped, UserColumn, TenantColumn):
    __tablename__ = "sessions"
    __table_args__ = ({"schema": "authn"},)

    username: Mapped[str] = acol(storage=S(String(120), nullable=False))
    client_id: Mapped[UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.clients.id"), nullable=True, index=True)
    )
    auth_time: Mapped[dt.datetime] = acol(
        storage=S(TZDateTime, nullable=False, default=lambda: dt.datetime.now(dt.timezone.utc))
    )
    session_state: Mapped[str] = acol(storage=S(String(64), nullable=False, default="active"))
    session_state_salt: Mapped[str | None] = acol(storage=S(String(128), nullable=True))
    cookie_secret_hash: Mapped[str | None] = acol(storage=S(String(128), nullable=True, index=True))
    cookie_issued_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True))
    cookie_rotated_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True))
    expires_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    last_seen_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True))
    ended_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    logout_reason: Mapped[str | None] = acol(storage=S(String(128), nullable=True))


__all__ = ["AuthSession"]
