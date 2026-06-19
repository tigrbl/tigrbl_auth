"""Durable resource-server contract and attestation registry."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import Base, GUIDPk, JSON, Mapped, S, String, Timestamped, acol

from ._ops import create_record, first_record, list_records, record_id, update_record


class ResourceServerContract(Base, GUIDPk, Timestamped):
    __tablename__ = "resource_server_contracts"
    __table_args__ = ({"schema": "authn"},)

    contract_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    resource_server_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    contract_kind: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    status: Mapped[str] = acol(storage=S(String(64), nullable=False, default="active", index=True))
    contract_payload: Mapped[dict] = acol(storage=S(JSON, nullable=False, default=dict))

    @classmethod
    async def register(cls, db: Any, **payload: Any) -> "ResourceServerContract":
        existing = await cls.lookup(db, contract_id=payload["contract_id"])
        payload.setdefault("contract_payload", dict(payload))
        payload.setdefault("status", "active")
        if existing is not None:
            return await update_record(cls, db, record_id(existing), payload)
        return await create_record(cls, db, payload)

    @classmethod
    async def lookup(cls, db: Any, *, contract_id: str) -> "ResourceServerContract | None":
        return await first_record(cls, db, {"contract_id": contract_id})

    @classmethod
    async def list_for_resource_server(cls, db: Any, *, resource_server_id: str) -> list["ResourceServerContract"]:
        return await list_records(cls, db, {"resource_server_id": resource_server_id})

    @classmethod
    async def disable(cls, db: Any, *, contract_id: str) -> "ResourceServerContract | None":
        row = await cls.lookup(db, contract_id=contract_id)
        if row is None:
            return None
        return await update_record(cls, db, record_id(row), {"status": "disabled"})


__all__ = ["ResourceServerContract"]
