"""Durable WebAuthn registration and authentication ceremony state."""

from __future__ import annotations

import datetime as dt

from tigrbl_identity_storage.framework import (
    GUIDPk,
    LargeBinary,
    Mapped,
    RestOltpTable,
    S,
    String,
    TZDateTime,
    Timestamped,
    acol,
)


class WebAuthnCeremony(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "webauthn_ceremonies"
    __table_args__ = {"extend_existing": True, "schema": "authn"}

    ceremony_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    tenant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    principal_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    ceremony_kind: Mapped[str] = acol(storage=S(String(32), nullable=False, index=True))
    rp_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    expected_origin: Mapped[str] = acol(storage=S(String(2048), nullable=False))
    challenge_digest: Mapped[bytes] = acol(storage=S(LargeBinary, nullable=False))
    options_digest: Mapped[bytes | None] = acol(storage=S(LargeBinary, nullable=True))
    user_verification_requirement: Mapped[str] = acol(storage=S(String(32), nullable=False, default="preferred"))
    resident_key_requirement: Mapped[str | None] = acol(storage=S(String(32), nullable=True))
    attestation_preference: Mapped[str | None] = acol(storage=S(String(32), nullable=True))
    state: Mapped[str] = acol(storage=S(String(32), nullable=False, default="pending", index=True))
    issued_at: Mapped[dt.datetime] = acol(storage=S(TZDateTime, nullable=False, index=True))
    expires_at: Mapped[dt.datetime] = acol(storage=S(TZDateTime, nullable=False, index=True))
    consumed_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    bound_credential_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    failure_code: Mapped[str | None] = acol(storage=S(String(128), nullable=True))


__all__ = ["WebAuthnCeremony"]
