"""Durable key rotation policy versions."""

from __future__ import annotations

import datetime as dt

from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, Boolean, Integer, Mapped, S, String, TZDateTime, Timestamped, acol



class KeyRotationPolicy(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "key_rotation_policies"
    __table_args__ = ({"schema": "authn"},)

    policy_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    version_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    tenant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    issuer: Mapped[str] = acol(storage=S(String(1000), nullable=False, index=True))
    profile: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    key_class: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    key_use: Mapped[str] = acol(storage=S(String(32), nullable=False, index=True))
    algorithm: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    cadence_days: Mapped[int] = acol(storage=S(Integer, nullable=False))
    max_key_age_days: Mapped[int] = acol(storage=S(Integer, nullable=False))
    overlap_seconds: Mapped[int] = acol(storage=S(Integer, nullable=False))
    retirement_seconds: Mapped[int] = acol(storage=S(Integer, nullable=False))
    approval_required: Mapped[bool] = acol(storage=S(Boolean, nullable=False, default=False))
    jwks_publish_required: Mapped[bool] = acol(storage=S(Boolean, nullable=False, default=True))
    created_by: Mapped[str] = acol(storage=S(String(255), nullable=False))
    reason: Mapped[str] = acol(storage=S(String(1000), nullable=False))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="draft", index=True))
    approved_by: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    approved_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True))
    published_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True))
    supersedes: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))


__all__ = ["KeyRotationPolicy"]
