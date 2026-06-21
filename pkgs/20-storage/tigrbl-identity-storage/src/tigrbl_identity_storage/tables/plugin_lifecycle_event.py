"""Append-only plugin lifecycle events."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, JSON, Mapped, S, String, Timestamped, acol

from ._ops import create_record, first_record, list_records


class PluginLifecycleEventRecord(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "plugin_lifecycle_events"
    __table_args__ = ({"schema": "authn"},)

    event_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    plugin_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    hook_name: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    outcome: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    message: Mapped[str | None] = acol(storage=S(String(2000), nullable=True))
    event_payload: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))

    @classmethod
    async def append_event(cls, db: Any, **payload: Any) -> "PluginLifecycleEventRecord":
        payload.setdefault("event_payload", dict(payload))
        return await create_record(cls, db, payload)

    @classmethod
    async def lookup(cls, db: Any, *, event_id: str) -> "PluginLifecycleEventRecord | None":
        return await first_record(cls, db, {"event_id": event_id})

    @classmethod
    async def list_for_plugin(cls, db: Any, *, plugin_id: str) -> list["PluginLifecycleEventRecord"]:
        return await list_records(cls, db, {"plugin_id": plugin_id})


__all__ = ["PluginLifecycleEventRecord"]
