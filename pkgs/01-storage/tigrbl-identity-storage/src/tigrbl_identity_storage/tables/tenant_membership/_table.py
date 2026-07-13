"""Durable principal-to-tenant memberships."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import (
    RestOltpTable,
    GUIDPk,
    JSON,
    Mapped,
    S,
    String,
    Timestamped,
    acol,
)


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
    status: Mapped[str] = acol(
        storage=S(String(32), nullable=False, default="active", index=True)
    )

    @classmethod
    async def grant_membership(
        cls, db, *, tenant_id: str, principal_id: str, roles=(), status: str = "active"
    ):
        from .._ops import create_record, first_record, record_id, update_record

        normalized = list(_str_tuple(roles))
        existing = await first_record(
            cls, db, {"tenant_id": tenant_id, "principal_id": principal_id}
        )
        payload = {
            "tenant_id": tenant_id,
            "principal_id": principal_id,
            "roles": normalized,
            "status": status,
        }
        if existing is None:
            return await create_record(cls, db, payload)
        return await update_record(cls, db, record_id(existing), payload)

    @classmethod
    async def assign_role(
        cls, db, *, tenant_id: str, principal_id: str, role_name: str
    ):
        from .._ops import field, first_record

        existing = await first_record(
            cls, db, {"tenant_id": tenant_id, "principal_id": principal_id}
        )
        roles = set(_str_tuple(field(existing, "roles", ()))) if existing else set()
        roles.add(role_name)
        return await cls.grant_membership(
            db,
            tenant_id=tenant_id,
            principal_id=principal_id,
            roles=roles,
            status="active",
        )

    @classmethod
    async def role_names_for_principal(
        cls, db, *, principal_id: str, tenant_id: str | None = None
    ) -> tuple[str, ...]:
        from .._ops import field, list_records

        filters = {"principal_id": principal_id}
        if tenant_id is not None:
            filters["tenant_id"] = tenant_id
        rows = await list_records(cls, db, filters)
        roles: set[str] = set()
        for row in rows:
            if field(row, "status", "active") == "active":
                roles.update(_str_tuple(field(row, "roles", ())))
        return tuple(sorted(roles))


__all__ = ["TenantMembership"]
