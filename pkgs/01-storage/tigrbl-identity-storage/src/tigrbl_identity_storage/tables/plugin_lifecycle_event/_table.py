"""Append-only plugin lifecycle events."""

from __future__ import annotations


from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, JSON, Mapped, S, String, Timestamped, acol



class PluginLifecycleEventRecord(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "plugin_lifecycle_events"
    __table_args__ = ({"schema": "authn"},)

    event_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    plugin_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    hook_name: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    outcome: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    message: Mapped[str | None] = acol(storage=S(String(2000), nullable=True))
    event_payload: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))


__all__ = ["PluginLifecycleEventRecord"]
