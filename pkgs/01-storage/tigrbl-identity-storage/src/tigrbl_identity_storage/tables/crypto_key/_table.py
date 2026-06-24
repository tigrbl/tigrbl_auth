"""Durable provider-neutral crypto key metadata."""

from __future__ import annotations

import uuid
from typing import Any

from tigrbl_identity_storage.framework import (
    Boolean,
    ForeignKeySpec,
    GUIDPk,
    Integer,
    JSON,
    Mapped,
    PgUUID,
    RestOltpTable,
    S,
    String,
    Timestamped,
    acol,
)

from .._ops import create_record, field, first_record, list_records, read_record, record_id, update_record, utc_now
from ._usage import normalize_payload_key_usage, stored_key_operations, stored_key_usages


class CryptoKey(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "crypto_keys"
    __table_args__ = ({"schema": "authn"},)

    kid: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    algorithm: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    key_kind: Mapped[str] = acol(storage=S(String(64), nullable=False, default="asymmetric", index=True))
    key_usages: Mapped[list[str] | None] = acol(storage=S(JSON, nullable=True))
    allowed_ops: Mapped[list[str] | None] = acol(storage=S(JSON, nullable=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))
    primary_version: Mapped[int | None] = acol(storage=S(Integer, nullable=True, default=1))
    provider: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    provider_key_ref: Mapped[str | None] = acol(storage=S(String(1000), nullable=True))
    export_policy: Mapped[str] = acol(storage=S(String(64), nullable=False, default="public_only", index=True))
    origin: Mapped[str] = acol(storage=S(String(64), nullable=False, default="generated", index=True))
    extractable: Mapped[bool] = acol(storage=S(Boolean, nullable=False, default=False))
    public_material_format: Mapped[str | None] = acol(storage=S(String(64), nullable=True))
    public_material: Mapped[dict | str | None] = acol(storage=S(JSON, nullable=True))
    fingerprint: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    key_metadata: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    tenant_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.tenants.id"), nullable=True, index=True)
    )
    realm_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.realms.id"), nullable=True, index=True)
    )


__all__ = ["CryptoKey"]
