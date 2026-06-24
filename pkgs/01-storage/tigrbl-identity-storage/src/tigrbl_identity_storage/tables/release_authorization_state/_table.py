"""Durable release authorization state and snapshots."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, JSON, Mapped, S, String, Timestamped, acol

from .._ops import create_record, first_record


class ReleaseAuthorizationState(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "release_authorization_states"
    __table_args__ = ({"schema": "authn"},)

    snapshot_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    release_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    subject: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    status: Mapped[str] = acol(storage=S(String(64), nullable=False, default="captured", index=True))
    state_payload: Mapped[dict] = acol(storage=S(JSON, nullable=False, default=dict))

    @classmethod
    async def snapshot(cls, db: Any, **payload: Any) -> "ReleaseAuthorizationState":
        payload.setdefault("state_payload", dict(payload))
        payload.setdefault("status", "captured")
        return await create_record(cls, db, payload)

    @classmethod
    async def lookup(cls, db: Any, *, snapshot_id: str) -> "ReleaseAuthorizationState | None":
        return await first_record(cls, db, {"snapshot_id": snapshot_id})

__all__ = ["ReleaseAuthorizationState"]
