"""Durable key attestation evidence metadata."""

from __future__ import annotations

import datetime as dt
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
    TZDateTime,
    Timestamped,
    acol,
)


class KeyAttestationEvidence(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "key_attestation_evidence"
    __table_args__ = ({"schema": "authn"},)

    key_id: Mapped[uuid.UUID] = acol(
        storage=S(
            PgUUID(as_uuid=True),
            fk=ForeignKeySpec(target="authn.crypto_keys.id"),
            nullable=False,
            index=True,
        )
    )
    key_version_id: Mapped[uuid.UUID | None] = acol(
        storage=S(
            PgUUID(as_uuid=True),
            fk=ForeignKeySpec(target="authn.crypto_key_versions.id"),
            nullable=True,
            index=True,
        )
    )
    issuer_key_id: Mapped[uuid.UUID | None] = acol(
        storage=S(
            PgUUID(as_uuid=True),
            fk=ForeignKeySpec(target="authn.crypto_keys.id"),
            nullable=True,
            index=True,
        )
    )
    issuer_provider: Mapped[str | None] = acol(
        storage=S(String(255), nullable=True, index=True)
    )
    evidence_format: Mapped[str] = acol(
        storage=S(String(64), nullable=False, index=True)
    )
    profile: Mapped[str | None] = acol(
        storage=S(String(255), nullable=True, index=True)
    )
    issuer: Mapped[str | None] = acol(
        storage=S(String(1000), nullable=True, index=True)
    )
    evidence_digest: Mapped[str | None] = acol(
        storage=S(String(128), nullable=True, index=True)
    )
    verification_result: Mapped[str | None] = acol(
        storage=S(String(64), nullable=True, index=True)
    )
    valid_until: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )
    evidence: Mapped[dict | str] = acol(storage=S(JSON, nullable=False))
    claims: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    status: Mapped[str] = acol(
        storage=S(String(32), nullable=False, default="unverified", index=True)
    )
    verified_at: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )
    evidence_metadata: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    tenant_id: Mapped[uuid.UUID | None] = acol(
        storage=S(
            PgUUID(as_uuid=True),
            fk=ForeignKeySpec(target="authn.tenants.id"),
            nullable=True,
            index=True,
        )
    )
    realm_id: Mapped[uuid.UUID | None] = acol(
        storage=S(
            PgUUID(as_uuid=True),
            fk=ForeignKeySpec(target="authn.realms.id"),
            nullable=True,
            index=True,
        )
    )


__all__ = ["KeyAttestationEvidence"]
