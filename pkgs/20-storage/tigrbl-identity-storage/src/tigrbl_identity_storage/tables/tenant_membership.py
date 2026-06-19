"""Durable principal-to-tenant memberships."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import Base, GUIDPk, JSON, Mapped, S, String, Timestamped, acol

from ._ops import create_record, first_record, list_records, record_id, update_record


class TenantMembership(Base, GUIDPk, Timestamped):
    __tablename__ = "tenant_memberships"
    __table_args__ = ({"schema": "authn"},)

    tenant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    principal_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    roles: Mapped[list | None] = acol(storage=S(JSON, nullable=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))

    @classmethod
    async def grant_membership(
        cls,
        db: Any,
        *,
        tenant_id: str,
        principal_id: str,
        roles: list[str] | tuple[str, ...] = (),
        status: str = "active",
    ) -> "TenantMembership":
        existing = await cls.lookup(db, tenant_id=tenant_id, principal_id=principal_id)
        payload = {"tenant_id": tenant_id, "principal_id": principal_id, "roles": list(roles), "status": status}
        if existing is not None:
            return await update_record(cls, db, record_id(existing), payload)
        return await create_record(cls, db, payload)

    @classmethod
    async def lookup(cls, db: Any, *, tenant_id: str, principal_id: str) -> "TenantMembership | None":
        return await first_record(cls, db, {"tenant_id": tenant_id, "principal_id": principal_id})

    @classmethod
    async def list_for_principal(cls, db: Any, *, principal_id: str) -> list["TenantMembership"]:
        return await list_records(cls, db, {"principal_id": principal_id})

    @classmethod
    async def revoke_membership(cls, db: Any, *, tenant_id: str, principal_id: str) -> "TenantMembership | None":
        row = await cls.lookup(db, tenant_id=tenant_id, principal_id=principal_id)
        if row is None:
            return None
        return await update_record(cls, db, record_id(row), {"status": "revoked"})


__all__ = ["TenantMembership"]
