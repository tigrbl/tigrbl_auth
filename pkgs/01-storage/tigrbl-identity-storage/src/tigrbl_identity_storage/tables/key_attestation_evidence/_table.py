"""Durable key attestation evidence metadata."""

from __future__ import annotations

import datetime as dt
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
    TZDateTime,
    Timestamped,
    acol,
)

from .._ops import create_record, list_records, update_record, utc_now


class KeyAttestationEvidence(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "key_attestation_evidence"
    __table_args__ = ({"schema": "authn"},)

    key_id: Mapped[uuid.UUID] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.crypto_keys.id"), nullable=False, index=True)
    )
    key_version_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.crypto_key_versions.id"), nullable=True, index=True)
    )
    issuer_key_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.crypto_keys.id"), nullable=True, index=True)
    )
    issuer_provider: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    evidence_format: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    evidence: Mapped[dict | str] = acol(storage=S(JSON, nullable=False))
    claims: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="unverified", index=True))
    verified_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    evidence_metadata: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    tenant_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.tenants.id"), nullable=True, index=True)
    )
    realm_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.realms.id"), nullable=True, index=True)
    )

    @classmethod
    async def record_evidence(
        cls,
        db: Any,
        *,
        key_id: uuid.UUID,
        evidence_format: str,
        evidence: dict | str,
        key_version_id: uuid.UUID | None = None,
        issuer_key_id: uuid.UUID | None = None,
        issuer_provider: str | None = None,
        claims: dict | None = None,
        status: str = "unverified",
        evidence_metadata: dict | None = None,
        tenant_id: uuid.UUID | None = None,
        realm_id: uuid.UUID | None = None,
    ) -> "KeyAttestationEvidence":
        return await create_record(
            cls,
            db,
            {
                "key_id": key_id,
                "key_version_id": key_version_id,
                "issuer_key_id": issuer_key_id,
                "issuer_provider": issuer_provider,
                "evidence_format": evidence_format,
                "evidence": evidence,
                "claims": claims,
                "status": status,
                "evidence_metadata": evidence_metadata,
                "tenant_id": tenant_id,
                "realm_id": realm_id,
            },
        )

    @classmethod
    async def list_for_key(cls, db: Any, *, key_id: uuid.UUID) -> list["KeyAttestationEvidence"]:
        return await list_records(cls, db, {"key_id": key_id})

    @classmethod
    async def mark_verified(cls, db: Any, *, id: Any, metadata: dict | None = None) -> "KeyAttestationEvidence":
        return await update_record(
            cls,
            db,
            id,
            {
                "status": "verified",
                "verified_at": utc_now(),
                "evidence_metadata": metadata,
            },
        )


__all__ = ["KeyAttestationEvidence"]
