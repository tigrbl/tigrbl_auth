"""Durable attestation evidence, results, reference material, and policies."""

from __future__ import annotations
import datetime as dt
from tigrbl_identity_storage.framework import (
    Boolean,
    GUIDPk,
    JSON,
    Mapped,
    RestOltpTable,
    S,
    String,
    TZDateTime,
    Timestamped,
    acol,
)


class AttestationEvidence(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "attestation_evidence"
    __table_args__ = ({"schema": "authn"},)
    evidence_id: Mapped[str] = acol(
        storage=S(String(255), nullable=False, unique=True, index=True)
    )
    profile: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    format: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    issuer: Mapped[str | None] = acol(
        storage=S(String(1000), nullable=True, index=True)
    )
    artifact_locator: Mapped[str] = acol(storage=S(String(1000), nullable=False))
    evidence_digest: Mapped[str] = acol(
        storage=S(String(128), nullable=False, index=True)
    )
    expires_at: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )


class AttestationResult(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "attestation_results"
    __table_args__ = ({"schema": "authn"},)
    evidence_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    policy_id: Mapped[str | None] = acol(
        storage=S(String(255), nullable=True, index=True)
    )
    trusted: Mapped[bool] = acol(storage=S(Boolean, nullable=False, index=True))
    reason: Mapped[str] = acol(storage=S(String(1000), nullable=False))
    result_claims: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    appraised_at: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )


class AttestationReferenceManifest(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "attestation_reference_manifests"
    __table_args__ = ({"schema": "authn"},)
    manifest_id: Mapped[str] = acol(
        storage=S(String(255), nullable=False, unique=True, index=True)
    )
    profile: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    format: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    artifact_locator: Mapped[str] = acol(storage=S(String(1000), nullable=False))
    artifact_digest: Mapped[str] = acol(
        storage=S(String(128), nullable=False, index=True)
    )
    signer: Mapped[str | None] = acol(
        storage=S(String(1000), nullable=True, index=True)
    )
    valid_until: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )


class AttestationReferenceValue(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "attestation_reference_values"
    __table_args__ = ({"schema": "authn"},)
    manifest_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    environment: Mapped[str] = acol(storage=S(String(1000), nullable=False, index=True))
    measurement_id: Mapped[str] = acol(
        storage=S(String(255), nullable=False, index=True)
    )
    algorithm: Mapped[str] = acol(storage=S(String(64), nullable=False))
    digest: Mapped[str] = acol(storage=S(String(256), nullable=False, index=True))


class AttestationEndorsement(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "attestation_endorsements"
    __table_args__ = ({"schema": "authn"},)
    endorsement_id: Mapped[str] = acol(
        storage=S(String(255), nullable=False, unique=True, index=True)
    )
    profile: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    issuer: Mapped[str] = acol(storage=S(String(1000), nullable=False, index=True))
    artifact_locator: Mapped[str] = acol(storage=S(String(1000), nullable=False))
    artifact_digest: Mapped[str] = acol(
        storage=S(String(128), nullable=False, index=True)
    )
    valid_until: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )


class AttestationAppraisalPolicy(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "attestation_appraisal_policies"
    __table_args__ = ({"schema": "authn"},)
    policy_id: Mapped[str] = acol(
        storage=S(String(255), nullable=False, unique=True, index=True)
    )
    profile: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    version: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    policy: Mapped[dict] = acol(storage=S(JSON, nullable=False))
    enabled: Mapped[bool] = acol(
        storage=S(Boolean, nullable=False, default=True, index=True)
    )


__all__ = [
    "AttestationEvidence",
    "AttestationResult",
    "AttestationReferenceManifest",
    "AttestationReferenceValue",
    "AttestationEndorsement",
    "AttestationAppraisalPolicy",
]
