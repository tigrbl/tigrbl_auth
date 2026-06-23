"""Durable principal-to-tenant memberships."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, JSON, Mapped, S, String, Timestamped, acol

from .._ops import create_record, first_record, list_records, record_id, update_record


def _str_tuple(values: Any) -> tuple[str, ...]:
    if values is None or values == "" or values is False:
        return ()
    if isinstance(values, str):
        return (values,)
    return tuple(sorted({str(value) for value in values if value not in {None, ""}}))


class TenantMembership(RestOltpTable, GUIDPk, Timestamped):
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
    async def assign_role(
        cls,
        db: Any,
        *,
        tenant_id: str,
        principal_id: str,
        role_name: str,
    ) -> "TenantMembership":
        membership = await cls.lookup(db, tenant_id=tenant_id, principal_id=principal_id)
        roles = set(_str_tuple(getattr(membership, "roles", None) if membership is not None else ()))
        if isinstance(membership, dict):
            roles = set(_str_tuple(membership.get("roles")))
        roles.add(role_name)
        return await cls.grant_membership(
            db,
            tenant_id=tenant_id,
            principal_id=principal_id,
            roles=tuple(sorted(roles)),
        )

    @classmethod
    async def role_names_for_principal(
        cls,
        db: Any,
        *,
        principal_id: str,
        tenant_id: str | None = None,
    ) -> tuple[str, ...]:
        roles: set[str] = set()
        for row in await cls.list_for_principal(db, principal_id=principal_id):
            row_status = row.get("status", "active") if isinstance(row, dict) else getattr(row, "status", "active")
            if str(row_status or "active") != "active":
                continue
            row_tenant_id = row.get("tenant_id") if isinstance(row, dict) else getattr(row, "tenant_id", None)
            if tenant_id is not None and row_tenant_id != tenant_id:
                continue
            row_roles = row.get("roles") if isinstance(row, dict) else getattr(row, "roles", None)
            roles.update(_str_tuple(row_roles))
        return tuple(sorted(roles))

    @classmethod
    async def revoke_membership(cls, db: Any, *, tenant_id: str, principal_id: str) -> "TenantMembership | None":
        row = await cls.lookup(db, tenant_id=tenant_id, principal_id=principal_id)
        if row is None:
            return None
        return await update_record(cls, db, record_id(row), {"status": "revoked"})


__all__ = ["TenantMembership"]
