"""Durable provider-neutral crypto key version metadata."""

from __future__ import annotations

import datetime as dt
import uuid
from typing import Any

from tigrbl_identity_storage.framework import (
    ForeignKeySpec,
    GUIDPk,
    Integer,
    JSON,
    Mapped,
    PgUUID,
    RestOltpTable,
    S,
    String,
    TZDateTime,
    Timestamped,
    acol,
)

from .._ops import create_record, first_record, list_records, record_id, update_record, utc_now


def _string_list(values: Any) -> list[str]:
    if values is None or values == "" or values is False:
        return []
    if isinstance(values, str):
        return [values]
    return [str(value) for value in values if value not in {None, ""}]


class CryptoKeyVersion(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "crypto_key_versions"
    __table_args__ = ({"schema": "authn"},)

    key_id: Mapped[uuid.UUID] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.crypto_keys.id"), nullable=False, index=True)
    )
    version: Mapped[int] = acol(storage=S(Integer, nullable=False, default=1))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))
    provider: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    provider_key_ref: Mapped[str | None] = acol(storage=S(String(1000), nullable=True))
    allowed_ops: Mapped[list[str] | None] = acol(storage=S(JSON, nullable=True))
    public_material_format: Mapped[str | None] = acol(storage=S(String(64), nullable=True))
    public_material: Mapped[dict | str | None] = acol(storage=S(JSON, nullable=True))
    fingerprint: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    not_before: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    not_after: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    activated_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    retired_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    version_metadata: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))

    @classmethod
    async def create_version(
        cls,
        db: Any,
        *,
        key_id: uuid.UUID,
        version: int,
        status: str = "active",
        public_material: dict | str | None = None,
        public_material_format: str | None = None,
        provider_key_ref: str | None = None,
        provider: str | None = None,
        allowed_ops: Any = None,
        fingerprint: str | None = None,
        not_before: dt.datetime | None = None,
        not_after: dt.datetime | None = None,
        activated_at: dt.datetime | None = None,
        retired_at: dt.datetime | None = None,
        version_metadata: dict | None = None,
    ) -> "CryptoKeyVersion":
        existing = await cls.lookup(db, key_id=key_id, version=version)
        payload = {
            "key_id": key_id,
            "version": version,
            "status": status,
            "public_material": public_material,
            "public_material_format": public_material_format,
            "provider_key_ref": provider_key_ref,
            "provider": provider,
            "allowed_ops": _string_list(allowed_ops),
            "fingerprint": fingerprint,
            "not_before": not_before,
            "not_after": not_after,
            "activated_at": activated_at,
            "retired_at": retired_at,
            "version_metadata": version_metadata,
        }
        if existing is not None:
            return await update_record(cls, db, record_id(existing), payload)
        return await create_record(cls, db, payload)

    @classmethod
    async def lookup(cls, db: Any, *, key_id: uuid.UUID, version: int) -> "CryptoKeyVersion | None":
        return await first_record(cls, db, {"key_id": key_id, "version": version})

    @classmethod
    async def list_for_key(cls, db: Any, *, key_id: uuid.UUID) -> list["CryptoKeyVersion"]:
        return await list_records(cls, db, {"key_id": key_id})

    @classmethod
    async def activate(cls, db: Any, *, key_id: uuid.UUID, version: int) -> "CryptoKeyVersion | None":
        row = await cls.lookup(db, key_id=key_id, version=version)
        if row is None:
            return None
        return await update_record(
            cls,
            db,
            record_id(row),
            {"status": "active", "activated_at": utc_now(), "retired_at": None},
        )

    @classmethod
    async def retire(cls, db: Any, *, key_id: uuid.UUID, version: int) -> "CryptoKeyVersion | None":
        row = await cls.lookup(db, key_id=key_id, version=version)
        if row is None:
            return None
        version_metadata = dict(getattr(row, "version_metadata", None) or {})
        retired_at = utc_now()
        version_metadata["retired_at"] = retired_at.isoformat()
        return await update_record(
            cls,
            db,
            record_id(row),
            {"status": "retired", "retired_at": retired_at, "version_metadata": version_metadata},
        )

    @classmethod
    async def export_public_material(cls, db: Any, *, key_id: uuid.UUID, version: int) -> dict[str, Any] | str | None:
        row = await cls.lookup(db, key_id=key_id, version=version)
        material = getattr(row, "public_material", None) if row is not None else None
        if isinstance(material, dict):
            return {key: value for key, value in material.items() if key not in {"d", "p", "q", "dp", "dq", "qi"}}
        return material if isinstance(material, str) else None


__all__ = ["CryptoKeyVersion"]
