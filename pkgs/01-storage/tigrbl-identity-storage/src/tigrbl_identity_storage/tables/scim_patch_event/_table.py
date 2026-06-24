"""Append-only SCIM patch operation events."""

from __future__ import annotations


from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, JSON, Mapped, S, String, Timestamped, acol



class ScimPatchEvent(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "scim_patch_events"
    __table_args__ = ({"schema": "authn"},)

    tenant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    resource_kind: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    resource_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    op: Mapped[str] = acol(storage=S(String(64), nullable=False))
    path: Mapped[str | None] = acol(storage=S(String(512), nullable=True))
    value_payload: Mapped[dict | list | str | int | float | bool | None] = acol(storage=S(JSON, nullable=True))


__all__ = ["ScimPatchEvent"]
