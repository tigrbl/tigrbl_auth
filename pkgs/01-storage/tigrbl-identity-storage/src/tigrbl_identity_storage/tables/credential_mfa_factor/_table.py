"""Durable MFA factor credential records."""

from __future__ import annotations


from tigrbl_identity_storage.framework import GUIDPk, JSON, Mapped, RestOltpTable, S, String, Timestamped, acol



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


__all__ = ["CredentialMfaFactor"]
