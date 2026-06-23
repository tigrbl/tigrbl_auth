"""Durable external subject aliases."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, Mapped, S, String, Timestamped, acol

from .._ops import create_record, first_record, list_records, record_id, update_record


class SubjectAlias(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "subject_aliases"
    __table_args__ = ({"schema": "authn"},)

    principal_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    issuer: Mapped[str] = acol(storage=S(String(1000), nullable=False, index=True))
    subject: Mapped[str] = acol(storage=S(String(1000), nullable=False, index=True))
    tenant_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    verified: Mapped[str] = acol(storage=S(String(8), nullable=False, default="false", index=True))

    @classmethod
    async def bind_alias(
        cls,
        db: Any,
        *,
        principal_id: str,
        issuer: str,
        subject: str,
        tenant_id: str | None = None,
        verified: bool = False,
    ) -> "SubjectAlias":
        existing = await cls.lookup(db, issuer=issuer, subject=subject, tenant_id=tenant_id)
        payload = {
            "principal_id": principal_id,
            "issuer": issuer,
            "subject": subject,
            "tenant_id": tenant_id,
            "verified": str(bool(verified)).lower(),
        }
        if existing is not None:
            return await update_record(cls, db, record_id(existing), payload)
        return await create_record(cls, db, payload)

    @classmethod
    async def lookup(
        cls,
        db: Any,
        *,
        issuer: str,
        subject: str,
        tenant_id: str | None = None,
    ) -> "SubjectAlias | None":
        filters: dict[str, Any] = {"issuer": issuer, "subject": subject}
        if tenant_id is not None:
            filters["tenant_id"] = tenant_id
        return await first_record(cls, db, filters)

    @classmethod
    async def list_for_principal(cls, db: Any, *, principal_id: str) -> list["SubjectAlias"]:
        return await list_records(cls, db, {"principal_id": principal_id})

    @classmethod
    async def verify_alias(cls, db: Any, *, issuer: str, subject: str, tenant_id: str | None = None) -> "SubjectAlias | None":
        row = await cls.lookup(db, issuer=issuer, subject=subject, tenant_id=tenant_id)
        if row is None:
            return None
        return await update_record(cls, db, record_id(row), {"verified": "true"})


__all__ = ["SubjectAlias"]
