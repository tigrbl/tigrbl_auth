"""Durable service identity records."""

from __future__ import annotations


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


__all__ = ["ServiceIdentity"]
