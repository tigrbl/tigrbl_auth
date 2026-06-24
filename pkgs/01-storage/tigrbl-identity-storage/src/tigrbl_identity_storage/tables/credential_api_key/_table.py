"""Durable API-key credential records."""

from __future__ import annotations


from tigrbl_identity_storage.framework import (
    Created,
    ColumnSpec,
    F,
    GUIDPk,
    IO,
    KeyDigest,
    LastUsed,
    ValidityWindow,
    RestOltpTable,
    S,
    acol,
    Mapped,
    String,
)


class CredentialApiKey(RestOltpTable, GUIDPk, Created, LastUsed, ValidityWindow, KeyDigest):
    __tablename__ = "credential_api_keys"
    __table_args__ = {"extend_existing": True, "schema": "authn"}

    label: Mapped[str] = acol(
        spec=ColumnSpec(
            storage=S(String, nullable=False),
            field=F(constraints={"max_length": 120}, required_in=("create",)),
            io=IO(in_verbs=("create",), out_verbs=("read", "list"), filter_ops=("eq",)),
        )
    )
    principal_id: Mapped[str] = acol(
        spec=ColumnSpec(
            storage=S(String(255), nullable=False, index=True),
            field=F(constraints={"max_length": 255}, required_in=("create",)),
            io=IO(in_verbs=("create",), out_verbs=("read", "list"), filter_ops=("eq",)),
        )
    )
    principal_kind: Mapped[str] = acol(
        spec=ColumnSpec(
            storage=S(String(64), nullable=False, default="user", index=True),
            field=F(constraints={"max_length": 64}, required_in=("create",)),
            io=IO(in_verbs=("create",), out_verbs=("read", "list"), filter_ops=("eq",)),
        )
    )


__all__ = ["CredentialApiKey"]
