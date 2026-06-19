"""Durable key rotation policy versions."""

from __future__ import annotations

import datetime as dt
from typing import Any

from tigrbl_identity_storage.framework import Base, GUIDPk, Boolean, Integer, Mapped, S, String, TZDateTime, Timestamped, acol

from ._ops import create_record, first_record, list_records, record_id, update_record, utc_now


class KeyRotationPolicy(Base, GUIDPk, Timestamped):
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

    @classmethod
    async def create_policy_version(cls, db: Any, **payload: Any) -> "KeyRotationPolicy":
        return await create_record(cls, db, payload)

    @classmethod
    async def lookup_version(cls, db: Any, *, version_id: str) -> "KeyRotationPolicy | None":
        return await first_record(cls, db, {"version_id": version_id})

    @classmethod
    async def list_for_tenant(cls, db: Any, *, tenant_id: str, status: str | None = None) -> list["KeyRotationPolicy"]:
        filters: dict[str, Any] = {"tenant_id": tenant_id}
        if status is not None:
            filters["status"] = status
        return await list_records(cls, db, filters)

    @classmethod
    async def approve(cls, db: Any, *, version_id: str, approved_by: str) -> "KeyRotationPolicy | None":
        row = await cls.lookup_version(db, version_id=version_id)
        if row is None:
            return None
        return await update_record(
            cls,
            db,
            record_id(row),
            {"status": "approved", "approved_by": approved_by, "approved_at": utc_now()},
        )

    @classmethod
    async def publish(cls, db: Any, *, version_id: str) -> "KeyRotationPolicy | None":
        row = await cls.lookup_version(db, version_id=version_id)
        if row is None:
            return None
        return await update_record(cls, db, record_id(row), {"status": "published", "published_at": utc_now()})


__all__ = ["KeyRotationPolicy"]
