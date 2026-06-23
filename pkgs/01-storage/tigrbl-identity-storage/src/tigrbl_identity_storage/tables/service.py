"""Service model for the authentication service."""

from __future__ import annotations

from tigrbl_identity_storage.framework import (
    RestOltpTable,
    GUIDPk,
    Timestamped,
    TenantBound,
    Principal,
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


class Service(RestOltpTable, GUIDPk, Timestamped, TenantBound, Principal, ActiveToggle):
    __tablename__ = "services"
    __table_args__ = ({"schema": "authn"},)

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
    _service_keys = relationship("ServiceKey", back_populates="_service", cascade="all, delete-orphan")


__all__ = ["Service"]
