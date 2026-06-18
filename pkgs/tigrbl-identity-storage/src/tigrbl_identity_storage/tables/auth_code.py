"""Authorization code model with browser-session linkage."""

from __future__ import annotations

import datetime as dt
from typing import Any

from tigrbl_identity_server.framework import (
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
from ._ops import create_record, read_record, record_id, update_record, utc_now


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

    @classmethod
    async def create_for_authorization(
        cls,
        db: Any,
        *,
        user_id: UUID,
        tenant_id: UUID,
        client_id: UUID,
        redirect_uri: str,
        expires_at: dt.datetime,
        session_id: UUID | None = None,
        code_challenge: str | None = None,
        nonce: str | None = None,
        scope: str | None = None,
        claims: dict | None = None,
    ) -> "AuthCode":
        return await create_record(
            cls,
            db,
            {
                "user_id": user_id,
                "tenant_id": tenant_id,
                "client_id": client_id,
                "session_id": session_id,
                "redirect_uri": redirect_uri,
                "code_challenge": code_challenge,
                "nonce": nonce,
                "scope": scope,
                "expires_at": expires_at,
                "claims": claims,
            },
        )

    @classmethod
    async def consume(cls, db: Any, *, code_id: UUID) -> "AuthCode | None":
        row = await read_record(cls, db, code_id)
        if row is None:
            return None
        return await update_record(cls, db, record_id(row) or code_id, {"expires_at": utc_now()})

    @classmethod
    async def expire(cls, db: Any, *, code_id: UUID) -> "AuthCode | None":
        row = await read_record(cls, db, code_id)
        if row is None:
            return None
        return await update_record(cls, db, record_id(row) or code_id, {"expires_at": utc_now()})


__all__ = ["AuthCode"]
