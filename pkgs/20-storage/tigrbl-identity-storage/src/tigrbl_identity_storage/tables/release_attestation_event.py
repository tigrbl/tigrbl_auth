"""Append-only release attestation events."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import Base, GUIDPk, JSON, Mapped, S, String, Timestamped, acol

from ._ops import create_record, first_record, list_records


class ReleaseAttestationEvent(Base, GUIDPk, Timestamped):
    __tablename__ = "release_attestation_events"
    __table_args__ = ({"schema": "authn"},)

    event_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    release_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    event_kind: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    subject: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    event_payload: Mapped[dict] = acol(storage=S(JSON, nullable=False, default=dict))

    @classmethod
    async def append_event(cls, db: Any, **payload: Any) -> "ReleaseAttestationEvent":
        payload.setdefault("event_payload", dict(payload))
        return await create_record(cls, db, payload)

    @classmethod
    async def lookup(cls, db: Any, *, event_id: str) -> "ReleaseAttestationEvent | None":
        return await first_record(cls, db, {"event_id": event_id})

    @classmethod
    async def list_for_release(cls, db: Any, *, release_id: str) -> list["ReleaseAttestationEvent"]:
        return await list_records(cls, db, {"release_id": release_id})


__all__ = ["ReleaseAttestationEvent"]
