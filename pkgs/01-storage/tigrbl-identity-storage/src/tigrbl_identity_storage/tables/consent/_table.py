"""Durable consent schema for scopes and claims grants."""

from __future__ import annotations

import datetime as dt

from tigrbl_identity_storage.framework import (
    ForeignKeySpec,
    GUIDPk,
    JSON,
    Mapped,
    PgUUID,
    RestOltpTable,
    S,
    String,
    TZDateTime,
    TenantColumn,
    Timestamped,
    UUID,
    UserColumn,
    acol,
)


class Consent(RestOltpTable, GUIDPk, Timestamped, UserColumn, TenantColumn):
    __tablename__ = "consents"
    __table_args__ = ({"schema": "authn"},)

    client_id: Mapped[UUID] = acol(
        storage=S(
            PgUUID(as_uuid=True),
            fk=ForeignKeySpec(target="authn.clients.id"),
            nullable=False,
            index=True,
        )
    )
    scope: Mapped[str] = acol(storage=S(String(1000), nullable=False))
    claims: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    state: Mapped[str] = acol(
        storage=S(String(32), nullable=False, default="active")
    )
    granted_at: Mapped[dt.datetime] = acol(
        storage=S(
            TZDateTime,
            nullable=False,
            default=lambda: dt.datetime.now(dt.timezone.utc),
        )
    )
    expires_at: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )
    revoked_at: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )


__all__ = ["Consent"]
