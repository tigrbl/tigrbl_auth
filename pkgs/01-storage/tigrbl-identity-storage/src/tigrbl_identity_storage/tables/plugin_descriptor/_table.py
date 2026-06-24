"""Durable plugin descriptor registry."""

from __future__ import annotations


from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, JSON, Mapped, S, String, Timestamped, acol



class PluginDescriptorRecord(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "plugin_descriptors"
    __table_args__ = ({"schema": "authn"},)

    plugin_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    name: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    version: Mapped[str] = acol(storage=S(String(128), nullable=False))
    isolation_mode: Mapped[str] = acol(storage=S(String(64), nullable=False))
    fail_behavior: Mapped[str] = acol(storage=S(String(64), nullable=False))
    descriptor_payload: Mapped[dict] = acol(storage=S(JSON, nullable=False, default=dict))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="enabled", index=True))


__all__ = ["PluginDescriptorRecord"]
