"""Durable authorization verification report artifacts."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import RestOltpTable, Boolean, GUIDPk, JSON, Mapped, S, String, Timestamped, acol

from ._ops import create_record, first_record, list_records


class AuthzVerificationReport(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "authz_verification_reports"
    __table_args__ = ({"schema": "authn"},)

    report_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    report_kind: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    tenant_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    passed: Mapped[bool | None] = acol(storage=S(Boolean, nullable=True, index=True))
    report_payload: Mapped[dict] = acol(storage=S(JSON, nullable=False, default=dict))

    @classmethod
    async def snapshot(cls, db: Any, **payload: Any) -> "AuthzVerificationReport":
        payload.setdefault("report_payload", dict(payload))
        return await create_record(cls, db, payload)

    @classmethod
    async def lookup(cls, db: Any, *, report_id: str) -> "AuthzVerificationReport | None":
        return await first_record(cls, db, {"report_id": report_id})

    @classmethod
    async def list_by_kind(cls, db: Any, *, report_kind: str) -> list["AuthzVerificationReport"]:
        return await list_records(cls, db, {"report_kind": report_kind})


__all__ = ["AuthzVerificationReport"]
