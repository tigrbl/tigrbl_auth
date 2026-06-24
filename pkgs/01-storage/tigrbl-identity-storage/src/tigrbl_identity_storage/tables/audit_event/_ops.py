from __future__ import annotations

__all__: list[str] = []

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx

import uuid
from .._ops import create_record, list_records, record_id, utc_now
from ..engine import storage_session
from ..tenant._table import Tenant
from ._table import AuditEvent
from typing import Any

async def _record(cls, db: Any, *, event_type: str, outcome: str = "success", **payload: Any) -> "AuditEvent":
    payload.update({"event_type": event_type, "outcome": outcome, "occurred_at": payload.get("occurred_at") or utc_now()})
    return await create_record(cls, db, payload)

@_table_op_ctx(bind=AuditEvent, alias="append_event", target="custom", rest=False)
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
        return await _record(cls,
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

# END classmethod-to-op_ctx migration
