"""Durable key version metadata."""

from __future__ import annotations

import uuid
from typing import Any

from tigrbl_identity_storage.framework import (
    RestOltpTable,
    ForeignKeySpec,
    GUIDPk,
    Integer,
    JSON,
    Mapped,
    PgUUID,
    S,
    String,
    Timestamped,
    acol,
)

from .._ops import create_record, first_record, list_records, record_id, update_record, utc_now


class KeyVersion(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "identity_key_versions"
    __table_args__ = ({"schema": "authn"},)

    key_id: Mapped[uuid.UUID] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.identity_keys.id"), nullable=False, index=True)
    )
    version: Mapped[int] = acol(storage=S(Integer, nullable=False, default=1))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))
    provider: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    provider_key_ref: Mapped[str | None] = acol(storage=S(String(1000), nullable=True))
    public_jwk: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    version_metadata: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))

    @classmethod
    async def create_version(
        cls,
        db: Any,
        *,
        key_id: uuid.UUID,
        version: int,
        status: str = "active",
        public_jwk: dict | None = None,
        provider_key_ref: str | None = None,
        provider: str | None = None,
        version_metadata: dict | None = None,
    ) -> "KeyVersion":
        existing = await cls.lookup(db, key_id=key_id, version=version)
        payload = {
            "key_id": key_id,
            "version": version,
            "status": status,
            "public_jwk": public_jwk,
            "provider_key_ref": provider_key_ref,
            "provider": provider,
            "version_metadata": version_metadata,
        }
        if existing is not None:
            return await update_record(cls, db, record_id(existing), payload)
        return await create_record(cls, db, payload)

    @classmethod
    async def lookup(cls, db: Any, *, key_id: uuid.UUID, version: int) -> "KeyVersion | None":
        return await first_record(cls, db, {"key_id": key_id, "version": version})

    @classmethod
    async def list_for_key(cls, db: Any, *, key_id: uuid.UUID) -> list["KeyVersion"]:
        return await list_records(cls, db, {"key_id": key_id})

    @classmethod
    async def activate(cls, db: Any, *, key_id: uuid.UUID, version: int) -> "KeyVersion | None":
        row = await cls.lookup(db, key_id=key_id, version=version)
        if row is None:
            return None
        return await update_record(cls, db, record_id(row), {"status": "active"})

    @classmethod
    async def retire(cls, db: Any, *, key_id: uuid.UUID, version: int) -> "KeyVersion | None":
        row = await cls.lookup(db, key_id=key_id, version=version)
        if row is None:
            return None
        version_metadata = dict(getattr(row, "version_metadata", None) or {})
        version_metadata["retired_at"] = utc_now().isoformat()
        return await update_record(cls, db, record_id(row), {"status": "retired", "version_metadata": version_metadata})

    @classmethod
    async def export_public_jwk(cls, db: Any, *, key_id: uuid.UUID, version: int) -> dict[str, Any] | None:
        row = await cls.lookup(db, key_id=key_id, version=version)
        if row is None or not isinstance(getattr(row, "public_jwk", None), dict):
            return None
        return {key: value for key, value in row.public_jwk.items() if key not in {"d", "p", "q", "dp", "dq", "qi"}}


__all__ = ["KeyVersion"]
