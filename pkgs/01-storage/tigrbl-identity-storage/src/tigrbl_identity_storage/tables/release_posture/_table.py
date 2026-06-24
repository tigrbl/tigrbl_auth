"""Durable release posture snapshots."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, JSON, Mapped, S, String, Timestamped, acol

from .._ops import create_record, first_record


class ReleasePosture(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "release_postures"
    __table_args__ = ({"schema": "authn"},)

    posture_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    release_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    posture_kind: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    status: Mapped[str] = acol(storage=S(String(64), nullable=False, default="captured", index=True))
    posture_payload: Mapped[dict] = acol(storage=S(JSON, nullable=False, default=dict))


__all__ = ["ReleasePosture"]
