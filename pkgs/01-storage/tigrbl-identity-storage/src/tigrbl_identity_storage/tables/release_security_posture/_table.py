"""Durable release security posture snapshots."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, JSON, Mapped, S, String, Timestamped, acol

from .._ops import create_record, first_record, list_records


class ReleaseSecurityPosture(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "release_security_postures"
    __table_args__ = ({"schema": "authn"},)

    posture_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    release_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    tenant_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    realm_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    status: Mapped[str] = acol(storage=S(String(64), nullable=False, default="captured", index=True))
    posture_payload: Mapped[dict] = acol(storage=S(JSON, nullable=False, default=dict))

    @classmethod
    async def snapshot(cls, db: Any, **payload: Any) -> "ReleaseSecurityPosture":
        payload.setdefault("posture_payload", dict(payload))
        payload.setdefault("status", "captured")
        return await create_record(cls, db, payload)

    @classmethod
    async def lookup(cls, db: Any, *, posture_id: str) -> "ReleaseSecurityPosture | None":
        return await first_record(cls, db, {"posture_id": posture_id})

    @classmethod
    async def list_for_release(cls, db: Any, *, release_id: str) -> list["ReleaseSecurityPosture"]:
        return await list_records(cls, db, {"release_id": release_id})


__all__ = ["ReleaseSecurityPosture"]
