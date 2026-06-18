"""Durable consent records for scopes and claims grants."""

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
    JSON,
    Mapped,
    String,
    TZDateTime,
    GUIDPk,
    ForeignKeySpec,
    PgUUID,
    UUID,
)
from ._ops import create_record, field, list_records, read_record, record_id, update_record, utc_now


class Consent(Base, GUIDPk, Timestamped, UserColumn, TenantColumn):
    __tablename__ = "consents"
    __table_args__ = ({"schema": "authn"},)

    client_id: Mapped[UUID] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.clients.id"), nullable=False, index=True)
    )
    scope: Mapped[str] = acol(storage=S(String(1000), nullable=False))
    claims: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    state: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active"))
    granted_at: Mapped[dt.datetime] = acol(
        storage=S(TZDateTime, nullable=False, default=lambda: dt.datetime.now(dt.timezone.utc))
    )
    expires_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    revoked_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))

    @classmethod
    async def grant(
        cls,
        db: Any,
        *,
        user_id: UUID,
        tenant_id: UUID,
        client_id: UUID,
        scope: str,
        claims: dict | None = None,
        expires_at: dt.datetime | None = None,
    ) -> "Consent":
        return await create_record(
            cls,
            db,
            {
                "user_id": user_id,
                "tenant_id": tenant_id,
                "client_id": client_id,
                "scope": scope,
                "claims": claims,
                "state": "active",
                "granted_at": utc_now(),
                "expires_at": expires_at,
            },
        )

    @classmethod
    async def list_for_user(
        cls,
        db: Any,
        *,
        user_id: UUID,
        tenant_id: UUID | None = None,
        active_only: bool = True,
    ) -> list["Consent"]:
        filters: dict[str, Any] = {"user_id": user_id}
        if tenant_id is not None:
            filters["tenant_id"] = tenant_id
        rows = await list_records(cls, db, filters)
        if not active_only:
            return rows
        now = utc_now()
        return [
            row
            for row in rows
            if field(row, "state", "active") == "active"
            and field(row, "revoked_at") is None
            and (field(row, "expires_at") is None or field(row, "expires_at") > now)
        ]

    @classmethod
    async def revoke_for_user(
        cls,
        db: Any,
        *,
        consent_id: UUID,
        user_id: UUID | None = None,
    ) -> "Consent | None":
        row = await read_record(cls, db, consent_id)
        if row is None or (user_id is not None and str(field(row, "user_id")) != str(user_id)):
            return None
        return await update_record(cls, db, record_id(row) or consent_id, {"state": "revoked", "revoked_at": utc_now()})

    @classmethod
    async def revoke_for_client(
        cls,
        db: Any,
        *,
        client_id: UUID,
        user_id: UUID | None = None,
        tenant_id: UUID | None = None,
    ) -> list["Consent"]:
        filters: dict[str, Any] = {"client_id": client_id}
        if user_id is not None:
            filters["user_id"] = user_id
        if tenant_id is not None:
            filters["tenant_id"] = tenant_id
        revoked = []
        for row in await list_records(cls, db, filters):
            updated = await update_record(cls, db, record_id(row), {"state": "revoked", "revoked_at": utc_now()})
            revoked.append(updated)
        return revoked


__all__ = ["Consent"]
