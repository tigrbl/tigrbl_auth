"""Durable release capability truth records."""

from __future__ import annotations


from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, JSON, Mapped, S, String, Timestamped, acol



class ReleaseCapabilityRecord(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "release_capability_records"
    __table_args__ = ({"schema": "authn"},)

    capability_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    release_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    name: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    status: Mapped[str] = acol(storage=S(String(64), nullable=False, default="recorded", index=True))
    capability_payload: Mapped[dict] = acol(storage=S(JSON, nullable=False, default=dict))


__all__ = ["ReleaseCapabilityRecord"]
