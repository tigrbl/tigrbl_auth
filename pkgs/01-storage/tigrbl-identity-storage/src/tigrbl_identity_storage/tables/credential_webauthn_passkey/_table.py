"""Durable WebAuthn passkey credential records."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import GUIDPk, Integer, JSON, Mapped, RestOltpTable, S, String, Timestamped, acol

from .._ops import create_record, first_record, list_records, record_id, update_record


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

    @classmethod
    async def bind_passkey(cls, db: Any, **payload: Any) -> "CredentialWebAuthnPasskey":
        return await create_record(cls, db, payload)

    @classmethod
    async def lookup_by_credential_id(
        cls,
        db: Any,
        *,
        webauthn_credential_id: str,
    ) -> "CredentialWebAuthnPasskey | None":
        return await first_record(cls, db, {"webauthn_credential_id": webauthn_credential_id})

    @classmethod
    async def list_for_principal(cls, db: Any, *, principal_id: str) -> list["CredentialWebAuthnPasskey"]:
        return await list_records(cls, db, {"principal_id": principal_id})

    @classmethod
    async def revoke(cls, db: Any, *, credential_id: str) -> "CredentialWebAuthnPasskey | None":
        row = await first_record(cls, db, {"credential_id": credential_id})
        if row is None:
            return None
        return await update_record(cls, db, record_id(row), {"status": "revoked"})


__all__ = ["CredentialWebAuthnPasskey"]
