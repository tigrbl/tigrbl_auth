"""Durable MFA factor credential records."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import GUIDPk, JSON, Mapped, RestOltpTable, S, String, Timestamped, acol

from .._ops import create_record, first_record, list_records, record_id, update_record


class CredentialMfaFactor(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "credential_mfa_factors"
    __table_args__ = {"extend_existing": True, "schema": "authn"}

    credential_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    principal_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    factor_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    method: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    secret_digest: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    public_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))
    factor_metadata: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))

    @classmethod
    async def bind_factor(cls, db: Any, **payload: Any) -> "CredentialMfaFactor":
        return await create_record(cls, db, payload)

    @classmethod
    async def lookup(cls, db: Any, *, factor_id: str) -> "CredentialMfaFactor | None":
        return await first_record(cls, db, {"factor_id": factor_id})

    @classmethod
    async def list_for_principal(cls, db: Any, *, principal_id: str) -> list["CredentialMfaFactor"]:
        return await list_records(cls, db, {"principal_id": principal_id})

    @classmethod
    async def revoke(cls, db: Any, *, credential_id: str) -> "CredentialMfaFactor | None":
        row = await first_record(cls, db, {"credential_id": credential_id})
        if row is None:
            return None
        return await update_record(cls, db, record_id(row), {"status": "revoked"})


__all__ = ["CredentialMfaFactor"]
