"""Durable WebAuthn passkey credential records."""

from __future__ import annotations


import datetime as dt

from tigrbl_identity_storage.framework import Boolean, GUIDPk, Integer, JSON, LargeBinary, Mapped, RestOltpTable, S, String, TZDateTime, Timestamped, acol



class CredentialWebAuthnPasskey(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "credential_webauthn_passkeys"
    __table_args__ = {"extend_existing": True, "schema": "authn"}

    credential_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    principal_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    webauthn_credential_id: Mapped[str] = acol(storage=S(String(1000), nullable=False, unique=True, index=True))
    public_key: Mapped[str] = acol(storage=S(String(4000), nullable=False))
    rp_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    algorithm: Mapped[str | None] = acol(storage=S(String(64), nullable=True))
    sign_count: Mapped[int] = acol(storage=S(Integer, nullable=False, default=0))
    transports: Mapped[list | None] = acol(storage=S(JSON, nullable=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))
    passkey_metadata: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    credential_external_id: Mapped[str | None] = acol(storage=S(String(1000), nullable=True, unique=True, index=True))
    credential_public_key_cose: Mapped[bytes | None] = acol(storage=S(LargeBinary, nullable=True))
    user_handle: Mapped[bytes | None] = acol(storage=S(LargeBinary, nullable=True, index=True))
    cose_algorithm: Mapped[int | None] = acol(storage=S(Integer, nullable=True))
    aaguid: Mapped[bytes | None] = acol(storage=S(LargeBinary, nullable=True, index=True))
    attestation_format: Mapped[str | None] = acol(storage=S(String(64), nullable=True))
    attestation_type: Mapped[str | None] = acol(storage=S(String(64), nullable=True))
    attestation_trust_status: Mapped[str | None] = acol(storage=S(String(32), nullable=True, index=True))
    discoverable: Mapped[bool] = acol(storage=S(Boolean, nullable=False, default=False, index=True))
    backup_eligible: Mapped[bool] = acol(storage=S(Boolean, nullable=False, default=False, index=True))
    backup_state: Mapped[bool] = acol(storage=S(Boolean, nullable=False, default=False, index=True))
    last_used_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    revoked_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    display_name: Mapped[str | None] = acol(storage=S(String(255), nullable=True))


__all__ = ["CredentialWebAuthnPasskey"]
