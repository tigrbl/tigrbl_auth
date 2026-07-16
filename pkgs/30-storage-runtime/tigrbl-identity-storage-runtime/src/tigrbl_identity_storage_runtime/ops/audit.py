"""Compatibility adapters for canonical audit durability operations."""

from typing import Any

from tigrbl_audit_durability.operations.audit import (
    append_audit_event_record,
    list_audit_event_records,
)


async def append_audit_event_async(*, db: Any | None = None, **payload: Any) -> Any:
    if db is not None:
        return await append_audit_event_record({"payload": payload, "db": db})
    from ..session import storage_session

    async with storage_session() as session:
        return await append_audit_event_record({"payload": payload, "db": session})


__all__ = [
    "append_audit_event_async",
    "append_audit_event_record",
    "list_audit_event_records",
]
