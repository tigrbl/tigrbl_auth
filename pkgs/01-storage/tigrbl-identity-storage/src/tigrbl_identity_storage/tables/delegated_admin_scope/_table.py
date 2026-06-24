"""Durable delegated administration scopes."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, JSON, Mapped, S, String, Timestamped, acol

from .._ops import create_record, first_record, list_records, record_id, update_record


class DelegatedAdminScope(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "delegated_admin_scopes"
    __table_args__ = ({"schema": "authn"},)

    subject: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    tenant_ids: Mapped[list] = acol(storage=S(JSON, nullable=False, default=list))
    permissions: Mapped[list] = acol(storage=S(JSON, nullable=False, default=list))
    visible_client_fields: Mapped[list | None] = acol(storage=S(JSON, nullable=True))
    mutable_client_fields: Mapped[list | None] = acol(storage=S(JSON, nullable=True))
    service_identity_permissions: Mapped[list | None] = acol(storage=S(JSON, nullable=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))


__all__ = ["DelegatedAdminScope"]
