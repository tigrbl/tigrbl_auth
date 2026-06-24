"""Durable wrapped data-key envelope metadata."""

from __future__ import annotations

import uuid

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


__all__ = ["KeyEnvelope"]
