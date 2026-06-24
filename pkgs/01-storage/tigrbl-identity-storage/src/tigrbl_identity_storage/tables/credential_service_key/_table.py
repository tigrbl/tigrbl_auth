"""Durable service-identity key credential records."""

from __future__ import annotations

from uuid import UUID

from tigrbl_identity_storage.framework import (
    ForeignKeySpec,
    Created,
    GUIDPk,
    KeyDigest,
    LastUsed,
    ValidityWindow,
    RestOltpTable,
    F,
    IO,
    S,
    acol,
    Mapped,
    PgUUID,
    String,
    relationship,
)


class CredentialServiceKey(RestOltpTable, GUIDPk, Created, LastUsed, ValidityWindow, KeyDigest):
    __tablename__ = "credential_service_keys"
    __table_args__ = {"extend_existing": True, "schema": "authn"}

    label: Mapped[str] = acol(
        storage=S(String, nullable=False),
        field=F(constraints={"max_length": 120}, required_in=("create",)),
        io=IO(in_verbs=("create",), out_verbs=("read", "list"), filter_ops=("eq",)),
    )
    service_identity_id: Mapped[UUID] = acol(
        storage=S(
            PgUUID(as_uuid=True),
            fk=ForeignKeySpec(target="authn.service_identities.id"),
            index=True,
            nullable=False,
        ),
        field=F(py_type=UUID, required_in=("create",)),
        io=IO(in_verbs=("create",), out_verbs=("read", "list"), filter_ops=("eq",)),
    )

    _service_identity = relationship("ServiceIdentity", back_populates="_credential_service_keys", lazy="joined")


__all__ = ["CredentialServiceKey"]
