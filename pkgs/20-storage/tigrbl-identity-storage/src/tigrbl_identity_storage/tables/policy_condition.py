"""Durable dynamic policy conditions."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, JSON, Mapped, S, String, Timestamped, acol

from ._ops import create_record, list_records


class PolicyCondition(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "policy_conditions"
    __table_args__ = ({"schema": "authn"},)

    policy_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    field_name: Mapped[str] = acol(storage=S(String(255), nullable=False))
    operator: Mapped[str] = acol(storage=S(String(64), nullable=False))
    expected: Mapped[dict | list | str | int | float | bool | None] = acol(storage=S(JSON, nullable=True))
    condition_metadata: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))

    @classmethod
    async def add_condition(
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

    @classmethod
    async def list_for_policy(cls, db: Any, *, policy_id: str) -> list["PolicyCondition"]:
        return await list_records(cls, db, {"policy_id": policy_id})


__all__ = ["PolicyCondition"]
