"""Durable credential audit events."""

from __future__ import annotations

import datetime as dt

from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, JSON, Mapped, S, String, TZDateTime, Timestamped, acol
from tigrbl_identity_core.clock import utc_now


class CredentialAuditEvent(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "credential_audit_events"
    __table_args__ = ({"schema": "authn"},)

    credential_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    action: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    principal_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    actor: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    outcome: Mapped[str] = acol(storage=S(String(32), nullable=False, default="ok", index=True))
    reason: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    occurred_at: Mapped[dt.datetime] = acol(storage=S(TZDateTime, nullable=False, default=utc_now))
    details: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))


__all__ = ["CredentialAuditEvent"]
