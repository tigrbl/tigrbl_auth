"""Durable SCIM user projection rows."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, JSON, Mapped, S, String, Timestamped, acol

from .._ops import create_record, first_record, list_records, record_id, update_record


class ScimUserRecord(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "scim_users"
    __table_args__ = ({"schema": "authn"},)

    user_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    tenant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    user_name: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    attributes: Mapped[dict] = acol(storage=S(JSON, nullable=False, default=dict))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))


__all__ = ["ScimUserRecord"]
