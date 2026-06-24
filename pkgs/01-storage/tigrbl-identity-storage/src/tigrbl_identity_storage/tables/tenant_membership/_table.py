"""Durable principal-to-tenant memberships."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, JSON, Mapped, S, String, Timestamped, acol

from .._ops import create_record, first_record, list_records, record_id, update_record


def _str_tuple(values: Any) -> tuple[str, ...]:
    if values is None or values == "" or values is False:
        return ()
    if isinstance(values, str):
        return (values,)
    return tuple(sorted({str(value) for value in values if value not in {None, ""}}))


class TenantMembership(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "tenant_memberships"
    __table_args__ = ({"schema": "authn"},)

    tenant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    principal_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    roles: Mapped[list | None] = acol(storage=S(JSON, nullable=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))


__all__ = ["TenantMembership"]
