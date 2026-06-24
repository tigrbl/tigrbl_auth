"""Durable principal registry records."""

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


class Principal(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "principals"
    __table_args__ = {"extend_existing": True, "schema": "authn"}

    principal_kind: Mapped[str] = acol(
        spec=ColumnSpec(
            storage=S(String(64), nullable=False, index=True),
            field=F(constraints={"max_length": 64}, required_in=("create",)),
            io=IO(in_verbs=("create", "update", "replace"), out_verbs=("read", "list"), filter_ops=("eq",)),
        )
    )
    subject: Mapped[str] = acol(
        spec=ColumnSpec(
            storage=S(String(1000), nullable=False, unique=True, index=True),
            field=F(constraints={"max_length": 1000}, required_in=("create",)),
            io=IO(in_verbs=("create", "update", "replace"), out_verbs=("read", "list"), filter_ops=("eq", "ilike")),
        )
    )
    tenant_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    realm_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    display_name: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))
    external_provider: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    external_ref: Mapped[str | None] = acol(storage=S(String(1000), nullable=True, index=True))
    principal_metadata: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))


__all__ = ["Principal"]
