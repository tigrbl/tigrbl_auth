"""Table-owned operator audit log."""

from __future__ import annotations

import json
from typing import Any, Mapping

from tigrbl_identity_storage.framework import Base, Mapped, S, String, acol

from ._ops import create_record, field, list_records


class OperatorAuditEvent(Base):
    __tablename__ = "operator_audit_events"

    id: Mapped[str] = acol(storage=S(String(255), primary_key=True, nullable=False))
    tenant_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    actor_user_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    actor_client_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    session_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    event_type: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    target_type: Mapped[str] = acol(storage=S(String(128), nullable=False))
    target_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    outcome: Mapped[str] = acol(storage=S(String(64), nullable=False))
    request_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    occurred_at: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    details_json: Mapped[str] = acol(storage=S(String(20000), nullable=False, default="{}"))

    @classmethod
    async def record_operator_audit(cls, db: Any, payload: Mapping[str, Any]) -> "OperatorAuditEvent":
        return await create_record(
            cls,
            db,
            {
                "id": payload.get("id"),
                "tenant_id": payload.get("tenant_id"),
                "actor_user_id": payload.get("actor_user_id"),
                "actor_client_id": payload.get("actor_client_id"),
                "session_id": payload.get("session_id"),
                "event_type": payload.get("event_type"),
                "target_type": payload.get("target_type"),
                "target_id": payload.get("target_id"),
                "outcome": payload.get("outcome"),
                "request_id": payload.get("request_id"),
                "occurred_at": payload.get("occurred_at"),
                "details_json": json.dumps(dict(payload.get("details") or {}), sort_keys=True),
            },
        )

    @classmethod
    async def list_operator_audit(cls, db: Any) -> list[dict[str, Any]]:
        rows = await list_records(cls, db)
        return [
            {
                "id": field(row, "id"),
                "tenant_id": field(row, "tenant_id"),
                "actor_user_id": field(row, "actor_user_id"),
                "actor_client_id": field(row, "actor_client_id"),
                "session_id": field(row, "session_id"),
                "event_type": field(row, "event_type"),
                "target_type": field(row, "target_type"),
                "target_id": field(row, "target_id"),
                "outcome": field(row, "outcome"),
                "request_id": field(row, "request_id"),
                "occurred_at": field(row, "occurred_at"),
                "details": json.loads(field(row, "details_json") or "{}"),
            }
            for row in sorted(rows, key=lambda item: (str(field(item, "occurred_at", "")), str(field(item, "id", ""))))
        ]


__all__ = ["OperatorAuditEvent"]
