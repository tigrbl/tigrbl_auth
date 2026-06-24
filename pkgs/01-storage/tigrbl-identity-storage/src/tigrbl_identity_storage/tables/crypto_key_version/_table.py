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
from tigrbl_security_trust_contracts import normalize_key_operations



def _operation_list(values: Any) -> list[str]:
    return [operation.value for operation in normalize_key_operations(values)]


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


__all__ = ["CryptoKeyVersion"]
