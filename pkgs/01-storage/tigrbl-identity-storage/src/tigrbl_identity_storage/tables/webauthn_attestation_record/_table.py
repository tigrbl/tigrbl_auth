"""Durable result of authenticator attestation appraisal."""

from __future__ import annotations

import datetime as dt

from tigrbl_identity_storage.framework import GUIDPk, LargeBinary, Mapped, RestOltpTable, S, String, TZDateTime, Timestamped, acol


class WebAuthnAttestationRecord(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "webauthn_attestation_records"
    __table_args__ = {"extend_existing": True, "schema": "authn"}

    attestation_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    credential_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    format: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    type: Mapped[str] = acol(storage=S(String(64), nullable=False))
    aaguid: Mapped[bytes | None] = acol(storage=S(LargeBinary, nullable=True, index=True))
    statement_digest: Mapped[bytes] = acol(storage=S(LargeBinary, nullable=False))
    certificate_chain_artifact_ref: Mapped[str | None] = acol(storage=S(String(1024), nullable=True))
    trust_anchor_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    metadata_statement_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    verification_status: Mapped[str] = acol(storage=S(String(32), nullable=False, index=True))
    verified_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    valid_until: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))


__all__ = ["WebAuthnAttestationRecord"]
