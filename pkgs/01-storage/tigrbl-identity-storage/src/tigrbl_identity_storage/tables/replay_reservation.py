"""Canonical protocol-neutral durable replay reservations."""

from __future__ import annotations

import datetime as dt

from tigrbl_identity_storage.framework import (
    GUIDPk,
    JSON,
    Mapped,
    RestOltpTable,
    S,
    String,
    TZDateTime,
    Timestamped,
    acol,
)


class ReplayReservation(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "replay_reservations"
    __table_args__ = ({"schema": "authn"},)

    namespace: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    key_digest: Mapped[str] = acol(
        storage=S(String(64), nullable=False, unique=True, index=True)
    )
    tenant_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    issuer: Mapped[str | None] = acol(storage=S(String(1000), nullable=True, index=True))
    expires_at: Mapped[dt.datetime] = acol(storage=S(TZDateTime, nullable=False, index=True))
    reservation_context: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))


__all__ = ["ReplayReservation"]
