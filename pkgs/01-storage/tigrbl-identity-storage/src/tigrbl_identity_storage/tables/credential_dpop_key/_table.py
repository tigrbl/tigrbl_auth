"""Durable DPoP key credential bindings."""

from __future__ import annotations


from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, JSON, Mapped, S, String, Timestamped, acol



class CredentialDpopKey(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "credential_dpop_keys"
    __table_args__ = ({"schema": "authn"},)

    credential_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    principal_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    jwk_thumbprint: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    public_jwk: Mapped[dict] = acol(storage=S(JSON, nullable=False))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))
    key_metadata: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))


__all__ = ["CredentialDpopKey"]
