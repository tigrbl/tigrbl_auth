"""Durable machine identity records."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import (
    ColumnSpec,
    F,
    GUIDPk,
    IO,
    JSON,
    Mapped,
    RestOltpTable,
    S,
    String,
    Timestamped,
    acol,
)

from .._ops import create_record, first_record, list_records, record_id, update_record


class MachineIdentity(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "machine_identities"
    __table_args__ = {"extend_existing": True, "schema": "authn"}

    principal_id: Mapped[str] = acol(
        spec=ColumnSpec(
            storage=S(String(255), nullable=False, unique=True, index=True),
            field=F(constraints={"max_length": 255}, required_in=("create",)),
            io=IO(in_verbs=("create", "update", "replace"), out_verbs=("read", "list"), filter_ops=("eq",)),
        )
    )
    machine_subject: Mapped[str] = acol(
        spec=ColumnSpec(
            storage=S(String(1000), nullable=False, unique=True, index=True),
            field=F(constraints={"max_length": 1000}, required_in=("create",)),
            io=IO(in_verbs=("create", "update", "replace"), out_verbs=("read", "list"), filter_ops=("eq", "ilike")),
        )
    )
    tenant_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    realm_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    hardware_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    attestation_type: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    trust_anchor: Mapped[str | None] = acol(storage=S(String(1000), nullable=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))
    machine_metadata: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))

    @classmethod
    async def create_identity(cls, db: Any, **payload: Any) -> "MachineIdentity":
        return await create_record(cls, db, payload)

    @classmethod
    async def lookup(cls, db: Any, *, principal_id: str) -> "MachineIdentity | None":
        return await first_record(cls, db, {"principal_id": principal_id})

    @classmethod
    async def lookup_by_subject(cls, db: Any, *, machine_subject: str) -> "MachineIdentity | None":
        return await first_record(cls, db, {"machine_subject": machine_subject})

    @classmethod
    async def list_for_tenant(cls, db: Any, *, tenant_id: str) -> list["MachineIdentity"]:
        return await list_records(cls, db, {"tenant_id": tenant_id})

    @classmethod
    async def disable(cls, db: Any, *, principal_id: str) -> "MachineIdentity | None":
        row = await cls.lookup(db, principal_id=principal_id)
        if row is None:
            return None
        return await update_record(cls, db, record_id(row), {"status": "disabled"})


__all__ = ["MachineIdentity"]
