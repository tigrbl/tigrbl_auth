"""Durable authorization verification report artifacts."""

from __future__ import annotations

from tigrbl_identity_storage.framework import (
    RestOltpTable,
    Boolean,
    GUIDPk,
    JSON,
    Mapped,
    S,
    String,
    Timestamped,
    acol,
)


class AuthzVerificationReport(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "authz_verification_reports"
    __table_args__ = ({"schema": "authn"},)

    report_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    report_kind: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    tenant_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    passed: Mapped[bool | None] = acol(storage=S(Boolean, nullable=True, index=True))
    report_payload: Mapped[dict] = acol(storage=S(JSON, nullable=False, default=dict))


__all__ = ["AuthzVerificationReport"]
