"""Consent-owned lifecycle helpers formerly exposed by storage persistence."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from .._ops import create_record
from .._sync import run_async
from ..engine import storage_session
from ._table import Consent


async def record_consent_async(
    *,
    user_id: UUID,
    tenant_id: UUID,
    client_id: UUID,
    scope: str,
    claims: dict[str, Any] | None = None,
    expires_at: datetime | None = None,
) -> Consent:
    async with storage_session() as db:
        return await create_record(
            Consent,
            db,
            {
                "user_id": user_id,
                "tenant_id": tenant_id,
                "client_id": client_id,
                "scope": scope,
                "claims": claims,
                "expires_at": expires_at,
                "state": "active",
            },
        )


async def revoke_consent_async(consent_id: UUID) -> Consent | None:
    async with storage_session() as db:
        return await Consent.revoke_for_user(db, consent_id=consent_id)


record_consent = lambda **kwargs: run_async(record_consent_async(**kwargs))
revoke_consent = lambda consent_id: run_async(revoke_consent_async(consent_id))


__all__ = ["record_consent", "record_consent_async", "revoke_consent", "revoke_consent_async"]

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx
from . import _table as _table_module

for _table_name in dir(_table_module):
    if not _table_name.startswith("__"):
        globals().setdefault(_table_name, getattr(_table_module, _table_name))

@_table_op_ctx(bind=Consent, alias="list_for_user", target="custom", rest=False)
async def list_for_user(
    cls,
    db: Any,
    *,
    user_id: UUID,
    tenant_id: UUID | None = None,
    active_only: bool = True,
) -> list["Consent"]:
    filters: dict[str, Any] = {"user_id": user_id}
    if tenant_id is not None:
        filters["tenant_id"] = tenant_id
    rows = await list_records(cls, db, filters)
    if not active_only:
        return rows
    now = utc_now()
    return [
        row
        for row in rows
        if field(row, "state", "active") == "active"
        and field(row, "revoked_at") is None
        and (field(row, "expires_at") is None or field(row, "expires_at") > now)
    ]

@_table_op_ctx(bind=Consent, alias="revoke_for_user", target="custom", rest=False)
async def revoke_for_user(
    cls,
    db: Any,
    *,
    consent_id: UUID,
    user_id: UUID | None = None,
) -> "Consent | None":
    row = await read_record(cls, db, consent_id)
    if row is None or (user_id is not None and str(field(row, "user_id")) != str(user_id)):
        return None
    return await update_record(cls, db, record_id(row) or consent_id, {"state": "revoked", "revoked_at": utc_now()})

@_table_op_ctx(bind=Consent, alias="revoke_for_client", target="custom", rest=False)
async def revoke_for_client(
    cls,
    db: Any,
    *,
    client_id: UUID,
    user_id: UUID | None = None,
    tenant_id: UUID | None = None,
) -> list["Consent"]:
    filters: dict[str, Any] = {"client_id": client_id}
    if user_id is not None:
        filters["user_id"] = user_id
    if tenant_id is not None:
        filters["tenant_id"] = tenant_id
    revoked = []
    for row in await list_records(cls, db, filters):
        updated = await update_record(cls, db, record_id(row), {"state": "revoked", "revoked_at": utc_now()})
        revoked.append(updated)
    return revoked

# END classmethod-to-op_ctx migration
