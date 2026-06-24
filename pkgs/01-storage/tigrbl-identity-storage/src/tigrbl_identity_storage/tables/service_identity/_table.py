"""Durable service identity records."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import (
    RestOltpTable,
    GUIDPk,
    Timestamped,
    TenantBound,
    Principal as PrincipalMixin,
    ActiveToggle,
    Mapped,
    String,
    relationship,
    F,
    IO,
    S,
    acol,
    ColumnSpec,
)
from .._ops import first_record, list_records, record_id, update_record


class ServiceIdentity(RestOltpTable, GUIDPk, Timestamped, TenantBound, PrincipalMixin, ActiveToggle):
    __tablename__ = "service_identities"
    __table_args__ = {"extend_existing": True, "schema": "authn"}

    name: Mapped[str] = acol(
        spec=ColumnSpec(
            storage=S(String(120), unique=True, nullable=False),
            field=F(constraints={"max_length": 120}, required_in=("create",)),
            io=IO(
                in_verbs=("create", "update", "replace"),
                out_verbs=("read", "list"),
                filter_ops=("eq", "ilike"),
                sortable=True,
            ),
        )
    )
    _credential_service_keys = relationship(
        "CredentialServiceKey",
        back_populates="_service_identity",
        cascade="all, delete-orphan",
    )

    @classmethod
    async def lookup(cls, db: Any, *, service_identity_id: Any) -> "ServiceIdentity | None":
        return await first_record(cls, db, {"id": service_identity_id})

    @classmethod
    async def list_for_tenant(cls, db: Any, *, tenant_id: Any) -> list["ServiceIdentity"]:
        return await list_records(cls, db, {"tenant_id": tenant_id})

    @classmethod
    async def disable(cls, db: Any, *, service_identity_id: Any) -> "ServiceIdentity | None":
        row = await cls.lookup(db, service_identity_id=service_identity_id)
        if row is None:
            return None
        return await update_record(cls, db, record_id(row), {"is_active": False})


__all__ = ["ServiceIdentity"]
