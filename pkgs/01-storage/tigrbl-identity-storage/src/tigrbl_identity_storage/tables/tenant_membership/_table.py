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
    op_ctx,
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



async def _grant_membership(cls, db, values):
    from .._ops import create_record, first_record, record_id, update_record

    tenant_id, principal_id = str(values["tenant_id"]), str(values["principal_id"])
    payload = {
        "tenant_id": tenant_id,
        "principal_id": principal_id,
        "roles": list(_str_tuple(values.get("roles", ()))),
        "status": str(values.get("status", "active")),
    }
    existing = await first_record(cls, db, {"tenant_id": tenant_id, "principal_id": principal_id})
    if existing is None:
        return await create_record(cls, db, payload)
    return await update_record(cls, db, record_id(existing), payload)


@op_ctx(bind=TenantMembership, alias="grant_membership", target="custom", arity="collection", rest=False)
async def grant_membership(cls, ctx):
    return await _grant_membership(cls, ctx["db"], dict(ctx.get("payload") or {}))


@op_ctx(bind=TenantMembership, alias="assign_role", target="custom", arity="collection", rest=False)
async def assign_role(cls, ctx):
    from .._ops import field, first_record

    values = dict(ctx.get("payload") or {})
    filters = {"tenant_id": values["tenant_id"], "principal_id": values["principal_id"]}
    existing = await first_record(cls, ctx["db"], filters)
    roles = set(_str_tuple(field(existing, "roles", ()))) if existing else set()
    roles.add(str(values["role_name"]))
    return await _grant_membership(cls, ctx["db"], {**filters, "roles": roles, "status": "active"})


@op_ctx(bind=TenantMembership, alias="role_names_for_principal", target="custom", arity="collection", rest=False)
async def role_names_for_principal(cls, ctx) -> tuple[str, ...]:
    from .._ops import field, list_records

    values = dict(ctx.get("payload") or {})
    filters = {"principal_id": values["principal_id"]}
    if values.get("tenant_id") is not None:
        filters["tenant_id"] = values["tenant_id"]
    rows = await list_records(cls, ctx["db"], filters)
    roles: set[str] = set()
    for row in rows:
        if field(row, "status", "active") == "active":
            roles.update(_str_tuple(field(row, "roles", ())))
    return tuple(sorted(roles))


__all__ = ["TenantMembership"]
