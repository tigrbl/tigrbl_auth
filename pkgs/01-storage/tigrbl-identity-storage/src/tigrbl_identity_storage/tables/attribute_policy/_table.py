"""Durable ABAC policy definitions."""

from __future__ import annotations


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


class AttributePolicy(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "attribute_policies"
    __table_args__ = ({"schema": "authn"},)

    name: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    tenant_id: Mapped[str | None] = acol(
        storage=S(String(255), nullable=True, index=True)
    )
    client_id: Mapped[str | None] = acol(
        storage=S(String(255), nullable=True, index=True)
    )
    permission: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    effect: Mapped[str] = acol(
        storage=S(String(32), nullable=False, default="allow", index=True)
    )
    required_attributes: Mapped[dict] = acol(
        storage=S(JSON, nullable=False, default=dict)
    )
    status: Mapped[str] = acol(
        storage=S(String(32), nullable=False, default="active", index=True)
    )



@op_ctx(bind=AttributePolicy, alias="upsert_with_conditions", target="custom", arity="collection", rest=False)
async def upsert_with_conditions(cls, ctx):
    from .._ops import create_record, clear_records, first_record, record_id, update_record
    from ..policy_condition import PolicyCondition

    values = dict(ctx.get("payload") or {})
    db = ctx["db"]
    existing = await first_record(cls, db, {"name": values["name"], "tenant_id": values.get("tenant_id")})
    payload = {
        "name": values["name"], "tenant_id": values.get("tenant_id"),
        "permission": values["permission"],
        "required_attributes": dict(values.get("required_attributes") or {}),
        "status": "active",
    }
    row = await create_record(cls, db, payload) if existing is None else await update_record(cls, db, record_id(existing), payload)
    policy_id = record_id(row)
    await clear_records(PolicyCondition, db, {"policy_id": policy_id})
    conditions = [await create_record(PolicyCondition, db, {"policy_id": policy_id, **dict(condition)}) for condition in values.get("dynamic_conditions", ())]
    return row, conditions


@op_ctx(bind=AttributePolicy, alias="list_active_with_conditions", target="custom", arity="collection", rest=False)
async def list_active_with_conditions(cls, ctx):
    from .._ops import list_records, record_id
    from ..policy_condition import PolicyCondition

    db = ctx["db"]
    tenant_id = (ctx.get("payload") or {}).get("tenant_id")
    rows = await list_records(cls, db, {"tenant_id": tenant_id, "status": "active"})
    return [(row, await list_records(PolicyCondition, db, {"policy_id": record_id(row)})) for row in rows]


__all__ = ["AttributePolicy"]
