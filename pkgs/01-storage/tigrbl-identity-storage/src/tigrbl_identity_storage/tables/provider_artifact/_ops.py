from __future__ import annotations

__all__: list[str] = []

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx

from .._ops import create_record, first_record, record_id, update_record
from ._table import ProviderArtifact
from typing import Any

@_table_op_ctx(bind=ProviderArtifact, alias="register", target="custom", rest=False)
async def register(cls, db: Any, **payload: Any) -> "ProviderArtifact":
    existing = await _lookup(cls, db, artifact_id=payload["artifact_id"])
    payload.setdefault("artifact_payload", dict(payload))
    payload.setdefault("status", "active")
    if existing is not None:
        return await update_record(cls, db, record_id(existing), payload)
    return await create_record(cls, db, payload)

async def _lookup(cls, db: Any, *, artifact_id: str) -> "ProviderArtifact | None":
    return await first_record(cls, db, {"artifact_id": artifact_id})

@_table_op_ctx(bind=ProviderArtifact, alias="disable", target="custom", rest=False)
async def disable(cls, db: Any, *, artifact_id: str) -> "ProviderArtifact | None":
    row = await _lookup(cls, db, artifact_id=artifact_id)
    if row is None:
        return None
    return await update_record(cls, db, record_id(row), {"status": "disabled"})

# END classmethod-to-op_ctx migration
