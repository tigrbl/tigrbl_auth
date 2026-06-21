"""Durable audit events for operator and protocol actions."""

from __future__ import annotations

import datetime as dt
import uuid
from typing import Any

from tigrbl_identity_storage.framework import (
    RestOltpTable,
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
from ._ops import create_record, list_records, record_id, utc_now
from ._session import storage_session
from ._sync import run_async
from .tenant import Tenant


class AuditEvent(RestOltpTable, GUIDPk, Timestamped, TenantColumn):
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

    @classmethod
    async def record(cls, db: Any, *, event_type: str, outcome: str = "success", **payload: Any) -> "AuditEvent":
        payload.update({"event_type": event_type, "outcome": outcome, "occurred_at": payload.get("occurred_at") or utc_now()})
        return await create_record(cls, db, payload)

    @classmethod
    async def list_for_subject(cls, db: Any, *, actor_user_id: uuid.UUID | None = None, actor_client_id: uuid.UUID | None = None) -> list["AuditEvent"]:
        filters: dict[str, Any] = {}
        if actor_user_id is not None:
            filters["actor_user_id"] = actor_user_id
        if actor_client_id is not None:
            filters["actor_client_id"] = actor_client_id
        return await list_records(cls, db, filters)

    @classmethod
    async def list_for_tenant(cls, db: Any, *, tenant_id: uuid.UUID) -> list["AuditEvent"]:
        return await list_records(cls, db, {"tenant_id": tenant_id})

    @classmethod
    async def append_event(
        cls,
        *,
        tenant_id: uuid.UUID | None = None,
        actor_user_id: uuid.UUID | None = None,
        actor_client_id: uuid.UUID | None = None,
        session_id: uuid.UUID | None = None,
        event_type: str,
        target_type: str | None = None,
        target_id: str | None = None,
        outcome: str = "success",
        request_id: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> "AuditEvent":
        async with storage_session() as db:
            effective_tenant_id = tenant_id
            if effective_tenant_id is None:
                tenants = await list_records(Tenant, db)
                if tenants:
                    effective_tenant_id = record_id(tenants[0])
            return await cls.record(
                db,
                tenant_id=effective_tenant_id,
                actor_user_id=actor_user_id,
                actor_client_id=actor_client_id,
                session_id=session_id,
                event_type=event_type,
                target_type=target_type,
                target_id=target_id,
                outcome=outcome,
                request_id=request_id,
                details=details,
            )


append_audit_event_async = AuditEvent.append_event
append_audit_event = lambda **kwargs: run_async(AuditEvent.append_event(**kwargs))


__all__ = ["AuditEvent", "append_audit_event", "append_audit_event_async"]
