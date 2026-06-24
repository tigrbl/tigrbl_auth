"""Durable principal-to-key binding metadata."""

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

from .._ops import first_record, list_records, update_record, utc_now


class PrincipalKeyBinding(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "principal_key_bindings"
    __table_args__ = ({"schema": "authn"},)

    principal_id: Mapped[uuid.UUID] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.principals.id"), nullable=False, index=True)
    )
    principal_kind: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    key_id: Mapped[uuid.UUID] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.crypto_keys.id"), nullable=False, index=True)
    )
    key_version_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.crypto_key_versions.id"), nullable=True, index=True)
    )
    binding_kind: Mapped[str] = acol(storage=S(String(64), nullable=False, default="identity", index=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))
    proof_metadata: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    binding_metadata: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    tenant_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.tenants.id"), nullable=True, index=True)
    )
    realm_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.realms.id"), nullable=True, index=True)
    )


__all__ = ["PrincipalKeyBinding"]
