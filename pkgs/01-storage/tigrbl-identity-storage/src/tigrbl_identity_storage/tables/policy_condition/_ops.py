from __future__ import annotations

__all__: list[str] = []

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx

from .._ops import clear_records, create_record
from ._table import PolicyCondition
from collections.abc import Mapping
from typing import Any, Iterable

async def _add_condition(
    cls,
    db: Any,
    *,
    policy_id: str,
    field_name: str,
    operator: str,
    expected: Any,
    condition_metadata: dict | None = None,
) -> "PolicyCondition":
    return await create_record(
        cls,
        db,
        {
            "policy_id": policy_id,
            "field_name": field_name,
            "operator": operator,
            "expected": expected,
            "condition_metadata": condition_metadata,
        },
    )

@_table_op_ctx(bind=PolicyCondition, alias="replace_for_policy", target="custom", rest=False)
async def replace_for_policy(
    cls,
    db: Any,
    *,
    policy_id: str,
    conditions: Iterable[Mapping[str, Any]],
) -> list["PolicyCondition"]:
    await clear_records(cls, db, {"policy_id": policy_id})
    rows: list["PolicyCondition"] = []
    for condition in conditions:
        rows.append(
            await _add_condition(cls,
                db,
                policy_id=policy_id,
                field_name=str(condition["field_name"]),
                operator=str(condition["operator"]),
                expected=condition.get("expected"),
                condition_metadata=dict(condition.get("condition_metadata") or {}),
            )
        )
    return rows

# END classmethod-to-op_ctx migration
