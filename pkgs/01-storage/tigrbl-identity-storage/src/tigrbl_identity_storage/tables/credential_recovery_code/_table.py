"""Durable recovery-code credential records."""

from __future__ import annotations

import datetime as dt
from typing import Any

from tigrbl_identity_storage.framework import GUIDPk, JSON, Mapped, RestOltpTable, S, String, TZDateTime, Timestamped, acol

from .._ops import first_record, list_records, record_id, update_record, utc_now


class CredentialRecoveryCode(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "credential_recovery_codes"
    __table_args__ = {"extend_existing": True, "schema": "authn"}

    credential_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    principal_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    code_digest: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))
    consumed_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    recovery_metadata: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))

    @classmethod
    async def lookup_active(cls, db: Any, *, code_digest: str) -> "CredentialRecoveryCode | None":
        return await first_record(cls, db, {"code_digest": code_digest, "status": "active"})

    @classmethod
    async def list_for_principal(cls, db: Any, *, principal_id: str) -> list["CredentialRecoveryCode"]:
        return await list_records(cls, db, {"principal_id": principal_id})

    @classmethod
    async def consume(cls, db: Any, *, code_digest: str) -> "CredentialRecoveryCode | None":
        row = await cls.lookup_active(db, code_digest=code_digest)
        if row is None:
            return None
        return await update_record(cls, db, record_id(row), {"status": "consumed", "consumed_at": utc_now()})

    @classmethod
    async def revoke(cls, db: Any, *, credential_id: str) -> list["CredentialRecoveryCode"]:
        rows = await list_records(cls, db, {"credential_id": credential_id})
        revoked = []
        for row in rows:
            revoked.append(await update_record(cls, db, record_id(row), {"status": "revoked"}))
        return revoked


__all__ = ["CredentialRecoveryCode"]
