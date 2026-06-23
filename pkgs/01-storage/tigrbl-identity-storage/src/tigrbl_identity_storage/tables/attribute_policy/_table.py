"""Durable ABAC policy definitions."""

from __future__ import annotations

from typing import Any, Iterable, Mapping

from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, JSON, Mapped, S, String, Timestamped, acol

from .._ops import create_record, first_record, list_records, record_id, update_record
from ..policy_condition import PolicyCondition


class AttributePolicy(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "attribute_policies"
    __table_args__ = ({"schema": "authn"},)

    name: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    tenant_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    client_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    permission: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    effect: Mapped[str] = acol(storage=S(String(32), nullable=False, default="allow", index=True))
    required_attributes: Mapped[dict] = acol(storage=S(JSON, nullable=False, default=dict))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))

    @classmethod
    async def create_policy(cls, db: Any, **payload: Any) -> "AttributePolicy":
        existing = await cls.lookup(db, name=payload["name"], tenant_id=payload.get("tenant_id"))
        payload.setdefault("status", "active")
        if existing is not None:
            return await update_record(cls, db, record_id(existing), payload)
        return await create_record(cls, db, payload)

    @classmethod
    async def lookup(cls, db: Any, *, name: str, tenant_id: str | None = None) -> "AttributePolicy | None":
        filters: dict[str, Any] = {"name": name}
        if tenant_id is not None:
            filters["tenant_id"] = tenant_id
        return await first_record(cls, db, filters)

    @classmethod
    async def list_for_permission(cls, db: Any, *, permission: str, tenant_id: str | None = None) -> list["AttributePolicy"]:
        filters: dict[str, Any] = {"permission": permission, "status": "active"}
        if tenant_id is not None:
            filters["tenant_id"] = tenant_id
        return await list_records(cls, db, filters)

    @classmethod
    async def list_active(cls, db: Any, *, tenant_id: str | None = None) -> list["AttributePolicy"]:
        filters: dict[str, Any] = {"status": "active"}
        if tenant_id is not None:
            filters["tenant_id"] = tenant_id
        return await list_records(cls, db, filters)

    @classmethod
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

    @classmethod
    async def list_active_with_conditions(
        cls,
        db: Any,
        *,
        tenant_id: str | None = None,
        client_id: str | None = None,
    ) -> tuple[tuple["AttributePolicy", tuple[PolicyCondition, ...]], ...]:
        rows: list[tuple["AttributePolicy", tuple[PolicyCondition, ...]]] = []
        for row in await cls.list_active(db, tenant_id=tenant_id):
            row_client_id = row.get("client_id") if isinstance(row, dict) else getattr(row, "client_id", None)
            if client_id is not None and row_client_id not in {None, client_id}:
                continue
            policy_id = str(record_id(row) or (row.get("name") if isinstance(row, dict) else getattr(row, "name", "")) or "")
            conditions = await PolicyCondition.list_for_policy(db, policy_id=policy_id)
            rows.append((row, tuple(conditions)))
        return tuple(rows)

    @classmethod
    async def disable(cls, db: Any, *, name: str, tenant_id: str | None = None) -> "AttributePolicy | None":
        row = await cls.lookup(db, name=name, tenant_id=tenant_id)
        if row is None:
            return None
        return await update_record(cls, db, record_id(row), {"status": "disabled"})


__all__ = ["AttributePolicy"]
