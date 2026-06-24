"""Append-only release attestation events."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, JSON, Mapped, S, String, Timestamped, acol

from .._ops import create_record, first_record


class ReleaseAttestationEvent(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "release_attestation_events"
    __table_args__ = ({"schema": "authn"},)

    event_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    release_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    event_kind: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    subject: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    event_payload: Mapped[dict] = acol(storage=S(JSON, nullable=False, default=dict))


__all__ = ["ReleaseAttestationEvent"]
