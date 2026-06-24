"""Durable entitlement assignments."""

from __future__ import annotations

import datetime as dt

from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, Mapped, S, String, TZDateTime, Timestamped, acol



class EntitlementAssignment(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "entitlement_assignments"
    __table_args__ = ({"schema": "authn"},)

    assignment_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    entitlement_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    tenant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    subject_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    justification: Mapped[str] = acol(storage=S(String(1000), nullable=False))
    assigned_by: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    expires_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))
    revoked_reason: Mapped[str | None] = acol(storage=S(String(1000), nullable=True))


__all__ = ["EntitlementAssignment"]
