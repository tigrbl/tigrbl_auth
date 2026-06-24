from __future__ import annotations

__all__: list[str] = []

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx
from . import _table as _table_module

for _table_name in dir(_table_module):
    if not _table_name.startswith("__"):
        globals().setdefault(_table_name, getattr(_table_module, _table_name))

@_table_op_ctx(bind=AttributePolicy, alias="create_policy", target="custom", rest=False)
async def create_policy(cls, db: Any, **payload: Any) -> "AttributePolicy":
    existing = await _lookup(cls, db, name=payload["name"], tenant_id=payload.get("tenant_id"))
    payload.setdefault("status", "active")
    if existing is not None:
        return await update_record(cls, db, record_id(existing), payload)
    return await create_record(cls, db, payload)

async def _lookup(cls, db: Any, *, name: str, tenant_id: str | None = None) -> "AttributePolicy | None":
    filters: dict[str, Any] = {"name": name}
    if tenant_id is not None:
        filters["tenant_id"] = tenant_id
    return await first_record(cls, db, filters)

async def _list_active(cls, db: Any, *, tenant_id: str | None = None) -> list["AttributePolicy"]:
    filters: dict[str, Any] = {"status": "active"}
    if tenant_id is not None:
        filters["tenant_id"] = tenant_id
    return await list_records(cls, db, filters)

@_table_op_ctx(bind=AttributePolicy, alias="upsert_with_conditions", target="custom", rest=False)
async def upsert_with_conditions(
    cls,
    db: Any,
    *,
    name: str,
    permission: str,
    required_attributes: Mapping[str, Any],
    tenant_id: str | None = None,
    dynamic_conditions: Iterable[Mapping[str, Any]] = (),
    effect: str = "allow",
    client_id: str | None = None,
) -> tuple["AttributePolicy", tuple[PolicyCondition, ...]]:
    row = await cls.create_policy(
        db,
        name=name,
        tenant_id=tenant_id,
        client_id=client_id,
        permission=permission,
        effect=effect,
        required_attributes=dict(required_attributes),
    )
    conditions = await PolicyCondition.replace_for_policy(
        db,
        policy_id=str(record_id(row) or name),
        conditions=tuple(dict(condition) for condition in dynamic_conditions),
    )
    return row, tuple(conditions)

@_table_op_ctx(bind=AttributePolicy, alias="list_active_with_conditions", target="custom", rest=False)
async def list_active_with_conditions(
    cls,
    db: Any,
    *,
    tenant_id: str | None = None,
    client_id: str | None = None,
) -> tuple[tuple["AttributePolicy", tuple[PolicyCondition, ...]], ...]:
    rows: list[tuple["AttributePolicy", tuple[PolicyCondition, ...]]] = []
    for row in await _list_active(cls, db, tenant_id=tenant_id):
        row_client_id = row.get("client_id") if isinstance(row, dict) else getattr(row, "client_id", None)
        if client_id is not None and row_client_id not in {None, client_id}:
            continue
        policy_id = str(record_id(row) or (row.get("name") if isinstance(row, dict) else getattr(row, "name", "")) or "")
        conditions = await list_records(PolicyCondition, db, {"policy_id": policy_id})
        rows.append((row, tuple(conditions)))
    return tuple(rows)

@_table_op_ctx(bind=AttributePolicy, alias="disable", target="custom", rest=False)
async def disable(cls, db: Any, *, name: str, tenant_id: str | None = None) -> "AttributePolicy | None":
    row = await _lookup(cls, db, name=name, tenant_id=tenant_id)
    if row is None:
        return None
    return await update_record(cls, db, record_id(row), {"status": "disabled"})

# END classmethod-to-op_ctx migration
