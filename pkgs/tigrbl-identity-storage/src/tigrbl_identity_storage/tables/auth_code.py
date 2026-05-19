"""Authorization code model with browser-session linkage."""

from __future__ import annotations

import datetime as dt

from tigrbl_auth.framework import (
    Base,
    TenantColumn,
    Timestamped,
    UserColumn,
    S,
    acol,
    ForeignKeySpec,
    JSON,
    PgUUID,
    String,
    TZDateTime,
    Mapped,
    UUID,
    GUIDPk,
)


class AuthCode(Base, GUIDPk, Timestamped, UserColumn, TenantColumn):
    __tablename__ = "auth_codes"
    __table_args__ = ({"schema": "authn"},)

    client_id: Mapped[UUID] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.clients.id"), nullable=False)
    )
    session_id: Mapped[UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.sessions.id"), nullable=True, index=True)
    )
    redirect_uri: Mapped[str] = acol(storage=S(String(1000), nullable=False))
    code_challenge: Mapped[str | None] = acol(storage=S(String, nullable=True))
    nonce: Mapped[str | None] = acol(storage=S(String, nullable=True))
    scope: Mapped[str | None] = acol(storage=S(String, nullable=True))
    expires_at: Mapped[dt.datetime] = acol(storage=S(TZDateTime, nullable=False))
    claims: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))


__all__ = ["AuthCode"]
