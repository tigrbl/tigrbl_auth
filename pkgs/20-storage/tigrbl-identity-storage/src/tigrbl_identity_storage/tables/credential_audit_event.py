"""Durable credential audit events."""

from __future__ import annotations

import datetime as dt
from typing import Any

from tigrbl_identity_storage.framework import Base, GUIDPk, JSON, Mapped, S, String, TZDateTime, Timestamped, acol

from ._ops import create_record, list_records, utc_now


class CredentialAuditEvent(Base, GUIDPk, Timestamped):
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

    @classmethod
    async def record(
        cls,
        db: Any,
        *,
        credential_id: str,
        action: str,
        principal_id: str | None = None,
        actor: str | None = None,
        outcome: str = "ok",
        reason: str | None = None,
        details: dict | None = None,
    ) -> "CredentialAuditEvent":
        return await create_record(
            cls,
            db,
            {
                "credential_id": credential_id,
                "action": action,
                "principal_id": principal_id,
                "actor": actor,
                "outcome": outcome,
                "reason": reason,
                "details": details,
            },
        )

    @classmethod
    async def list_for_credential(cls, db: Any, *, credential_id: str) -> list["CredentialAuditEvent"]:
        return await list_records(cls, db, {"credential_id": credential_id})

    @classmethod
    async def list_for_principal(cls, db: Any, *, principal_id: str) -> list["CredentialAuditEvent"]:
        return await list_records(cls, db, {"principal_id": principal_id})


__all__ = ["CredentialAuditEvent"]
