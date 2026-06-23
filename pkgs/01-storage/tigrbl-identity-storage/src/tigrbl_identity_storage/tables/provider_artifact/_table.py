"""Durable provider artifact and descriptor registry."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, JSON, Mapped, S, String, Timestamped, acol

from .._ops import create_record, first_record, list_records, record_id, update_record


class ProviderArtifact(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "provider_artifacts"
    __table_args__ = ({"schema": "authn"},)

    artifact_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    artifact_kind: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    provider_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    tenant_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    status: Mapped[str] = acol(storage=S(String(64), nullable=False, default="active", index=True))
    artifact_payload: Mapped[dict] = acol(storage=S(JSON, nullable=False, default=dict))

    @classmethod
    async def register(cls, db: Any, **payload: Any) -> "ProviderArtifact":
        existing = await cls.lookup(db, artifact_id=payload["artifact_id"])
        payload.setdefault("artifact_payload", dict(payload))
        payload.setdefault("status", "active")
        if existing is not None:
            return await update_record(cls, db, record_id(existing), payload)
        return await create_record(cls, db, payload)

    @classmethod
    async def lookup(cls, db: Any, *, artifact_id: str) -> "ProviderArtifact | None":
        return await first_record(cls, db, {"artifact_id": artifact_id})

    @classmethod
    async def list_by_kind(cls, db: Any, *, artifact_kind: str) -> list["ProviderArtifact"]:
        return await list_records(cls, db, {"artifact_kind": artifact_kind})

    @classmethod
    async def disable(cls, db: Any, *, artifact_id: str) -> "ProviderArtifact | None":
        row = await cls.lookup(db, artifact_id=artifact_id)
        if row is None:
            return None
        return await update_record(cls, db, record_id(row), {"status": "disabled"})


__all__ = ["ProviderArtifact"]
