"""Durable SCIM schema registry."""

from __future__ import annotations


from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, JSON, Mapped, S, String, Timestamped, acol



class ScimSchemaRecord(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "scim_schemas"
    __table_args__ = ({"schema": "authn"},)

    schema_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    resource_kind: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    required_fields: Mapped[list] = acol(storage=S(JSON, nullable=False, default=list))
    schema_payload: Mapped[dict] = acol(storage=S(JSON, nullable=False, default=dict))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))


__all__ = ["ScimSchemaRecord"]
