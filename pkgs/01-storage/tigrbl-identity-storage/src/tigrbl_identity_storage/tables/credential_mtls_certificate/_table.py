"""Durable mTLS credential bindings."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, JSON, Mapped, S, String, Timestamped, acol

from .._ops import first_record, list_records, record_id, update_record


class CredentialMtlsCertificate(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "credential_mtls_certificates"
    __table_args__ = ({"schema": "authn"},)

    credential_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    principal_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    certificate_thumbprint: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    subject_dn: Mapped[str | None] = acol(storage=S(String(1000), nullable=True))
    san_dns: Mapped[list | None] = acol(storage=S(JSON, nullable=True))
    san_uri: Mapped[list | None] = acol(storage=S(JSON, nullable=True))
    san_ip: Mapped[list | None] = acol(storage=S(JSON, nullable=True))
    san_email: Mapped[list | None] = acol(storage=S(JSON, nullable=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))
    certificate_metadata: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))

    @classmethod
    async def list_for_principal(cls, db: Any, *, principal_id: str) -> list["CredentialMtlsCertificate"]:
        return await list_records(cls, db, {"principal_id": principal_id})

    @classmethod
    async def revoke(cls, db: Any, *, credential_id: str) -> "CredentialMtlsCertificate | None":
        row = await first_record(cls, db, {"credential_id": credential_id})
        if row is None:
            return None
        return await update_record(cls, db, record_id(row), {"status": "revoked"})


__all__ = ["CredentialMtlsCertificate"]
