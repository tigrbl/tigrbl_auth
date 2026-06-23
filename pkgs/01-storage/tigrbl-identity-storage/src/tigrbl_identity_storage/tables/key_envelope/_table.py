"""Durable wrapped data-key envelope metadata."""

from __future__ import annotations

import uuid
from typing import Any

from tigrbl_identity_storage.framework import (
    ForeignKeySpec,
    GUIDPk,
    JSON,
    Mapped,
    PgUUID,
    RestOltpTable,
    S,
    String,
    Timestamped,
    acol,
)

from .._ops import create_record, first_record, list_records, update_record


class KeyEnvelope(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "key_envelopes"
    __table_args__ = ({"schema": "authn"},)

    envelope_label: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    wrapping_key_id: Mapped[uuid.UUID] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.crypto_keys.id"), nullable=False, index=True)
    )
    wrapping_key_version_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.crypto_key_versions.id"), nullable=True, index=True)
    )
    wrapped_key_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.crypto_keys.id"), nullable=True, index=True)
    )
    wrapped_key_version_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.crypto_key_versions.id"), nullable=True, index=True)
    )
    algorithm: Mapped[str] = acol(storage=S(String(128), nullable=False, index=True))
    material_format: Mapped[str] = acol(storage=S(String(64), nullable=False, default="wrapped", index=True))
    wrapped_material: Mapped[dict | str] = acol(storage=S(JSON, nullable=False))
    aad_hash: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))
    envelope_context: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    envelope_metadata: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    tenant_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.tenants.id"), nullable=True, index=True)
    )
    realm_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.realms.id"), nullable=True, index=True)
    )

    @classmethod
    async def record_envelope(
        cls,
        db: Any,
        *,
        wrapping_key_id: uuid.UUID,
        algorithm: str,
        wrapped_material: dict | str,
        wrapping_key_version_id: uuid.UUID | None = None,
        wrapped_key_id: uuid.UUID | None = None,
        wrapped_key_version_id: uuid.UUID | None = None,
        envelope_label: str | None = None,
        material_format: str = "wrapped",
        aad_hash: str | None = None,
        status: str = "active",
        envelope_context: dict | None = None,
        envelope_metadata: dict | None = None,
        tenant_id: uuid.UUID | None = None,
        realm_id: uuid.UUID | None = None,
    ) -> "KeyEnvelope":
        return await create_record(
            cls,
            db,
            {
                "envelope_label": envelope_label,
                "wrapping_key_id": wrapping_key_id,
                "wrapping_key_version_id": wrapping_key_version_id,
                "wrapped_key_id": wrapped_key_id,
                "wrapped_key_version_id": wrapped_key_version_id,
                "algorithm": algorithm,
                "material_format": material_format,
                "wrapped_material": wrapped_material,
                "aad_hash": aad_hash,
                "status": status,
                "envelope_context": envelope_context,
                "envelope_metadata": envelope_metadata,
                "tenant_id": tenant_id,
                "realm_id": realm_id,
            },
        )

    @classmethod
    async def lookup_by_label(cls, db: Any, *, envelope_label: str, tenant_id: uuid.UUID | None = None) -> "KeyEnvelope | None":
        filters: dict[str, Any] = {"envelope_label": envelope_label}
        if tenant_id is not None:
            filters["tenant_id"] = tenant_id
        return await first_record(cls, db, filters)

    @classmethod
    async def list_for_wrapping_key(cls, db: Any, *, wrapping_key_id: uuid.UUID) -> list["KeyEnvelope"]:
        return await list_records(cls, db, {"wrapping_key_id": wrapping_key_id})

    @classmethod
    async def disable(cls, db: Any, *, id: Any) -> "KeyEnvelope":
        return await update_record(cls, db, id, {"status": "disabled"})


__all__ = ["KeyEnvelope"]
