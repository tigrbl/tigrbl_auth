"""Durable workload identity records."""

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

from .._ops import first_record, list_records, record_id, update_record


class WorkloadIdentity(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "workload_identities"
    __table_args__ = {"extend_existing": True, "schema": "authn"}

    principal_id: Mapped[str] = acol(
        spec=ColumnSpec(
            storage=S(String(255), nullable=False, unique=True, index=True),
            field=F(constraints={"max_length": 255}, required_in=("create",)),
            io=IO(in_verbs=("create", "update", "replace"), out_verbs=("read", "list"), filter_ops=("eq",)),
        )
    )
    workload_subject: Mapped[str] = acol(
        spec=ColumnSpec(
            storage=S(String(1000), nullable=False, unique=True, index=True),
            field=F(constraints={"max_length": 1000}, required_in=("create",)),
            io=IO(in_verbs=("create", "update", "replace"), out_verbs=("read", "list"), filter_ops=("eq", "ilike")),
        )
    )
    tenant_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    realm_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    trust_domain: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    namespace: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    service_account: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    cloud_provider: Mapped[str | None] = acol(storage=S(String(64), nullable=True, index=True))
    cloud_subject: Mapped[str | None] = acol(storage=S(String(1000), nullable=True, index=True))
    image_digest: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))
    workload_metadata: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))


__all__ = ["WorkloadIdentity"]
