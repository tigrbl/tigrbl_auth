"""Durable credential lifecycle records."""

from __future__ import annotations

import datetime as dt
from typing import Any

from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, Integer, JSON, Mapped, S, String, TZDateTime, Timestamped, acol

from ._ops import create_record, field, first_record, list_records, record_id, update_record, utc_now


class Credential(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "credentials"
    __table_args__ = ({"schema": "authn"},)

    principal_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    credential_kind: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    secret_digest: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    public_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))
    version: Mapped[int] = acol(storage=S(Integer, nullable=False, default=1))
    rotated_from: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    expires_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    credential_metadata: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))

    @classmethod
    async def create_credential(
        cls,
        db: Any,
        *,
        principal_id: str,
        credential_kind: str,
        secret_digest: str | None = None,
        public_id: str | None = None,
        status: str = "active",
        version: int = 1,
        rotated_from: str | None = None,
        expires_at: dt.datetime | None = None,
        credential_metadata: dict | None = None,
    ) -> "Credential":
        return await create_record(
            cls,
            db,
            {
                "principal_id": principal_id,
                "credential_kind": credential_kind,
                "secret_digest": secret_digest,
                "public_id": public_id,
                "status": status,
                "version": version,
                "rotated_from": rotated_from,
                "expires_at": expires_at,
                "credential_metadata": credential_metadata,
            },
        )

    @classmethod
    async def lookup_active(
        cls,
        db: Any,
        *,
        principal_id: str | None = None,
        public_id: str | None = None,
        secret_digest: str | None = None,
        credential_kind: str | None = None,
    ) -> "Credential | None":
        filters: dict[str, Any] = {"status": "active"}
        if principal_id is not None:
            filters["principal_id"] = principal_id
        if public_id is not None:
            filters["public_id"] = public_id
        if secret_digest is not None:
            filters["secret_digest"] = secret_digest
        if credential_kind is not None:
            filters["credential_kind"] = credential_kind
        row = await first_record(cls, db, filters)
        if row is None:
            return None
        expires_at = field(row, "expires_at")
        if isinstance(expires_at, dt.datetime) and expires_at <= utc_now():
            return None
        return row

    @classmethod
    async def list_for_principal(
        cls,
        db: Any,
        *,
        principal_id: str,
        credential_kind: str | None = None,
        status: str | None = None,
    ) -> list["Credential"]:
        filters: dict[str, Any] = {"principal_id": principal_id}
        if credential_kind is not None:
            filters["credential_kind"] = credential_kind
        if status is not None:
            filters["status"] = status
        return await list_records(cls, db, filters)

    @classmethod
    async def rotate(
        cls,
        db: Any,
        *,
        id: Any,
        secret_digest: str | None = None,
        public_id: str | None = None,
        credential_metadata: dict | None = None,
    ) -> "Credential":
        row = await update_record(cls, db, id, {"status": "rotated"})
        return await cls.create_credential(
            db,
            principal_id=field(row, "principal_id"),
            credential_kind=field(row, "credential_kind"),
            secret_digest=secret_digest,
            public_id=public_id,
            version=int(field(row, "version", 1) or 1) + 1,
            rotated_from=str(record_id(row)),
            credential_metadata=credential_metadata,
        )

    @classmethod
    async def revoke(cls, db: Any, *, id: Any, reason: str | None = None) -> "Credential":
        meta = {"revoked_at": utc_now().isoformat()}
        if reason:
            meta["revoked_reason"] = reason
        return await update_record(cls, db, id, {"status": "revoked", "credential_metadata": meta})


__all__ = ["Credential"]
