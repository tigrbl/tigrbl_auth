"""ClientRegistration-owned lifecycle helpers formerly exposed by storage persistence."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable
from uuid import UUID

from .._ops import create_handler_record, field, first_handler_record, record_id, update_handler_record
from .._sync import run_async
from ..engine import storage_session
from ._table import ClientRegistration


async def get_client_registration_async(client_id: UUID) -> ClientRegistration | None:
    async with storage_session() as db:
        return await first_handler_record(ClientRegistration, db, {"client_id": client_id})


async def upsert_client_registration_async(
    *,
    client_id: UUID,
    tenant_id: UUID | None = None,
    metadata: dict[str, Any] | None = None,
    contacts: Iterable[str] | None = None,
    software_id: str | None = None,
    software_version: str | None = None,
    registration_access_token_hash: str | None = None,
    registration_client_uri: str | None = None,
) -> ClientRegistration:
    async with storage_session() as db:
        row = await first_handler_record(ClientRegistration, db, {"client_id": client_id})
        payload = {
            "client_id": client_id,
            "tenant_id": tenant_id or field(row, "tenant_id"),
            "registration_metadata": metadata or field(row, "registration_metadata"),
            "contacts": list(contacts) if contacts is not None else field(row, "contacts"),
            "software_id": software_id or field(row, "software_id"),
            "software_version": software_version or field(row, "software_version"),
            "registration_access_token_hash": registration_access_token_hash
            or field(row, "registration_access_token_hash"),
            "registration_client_uri": registration_client_uri or field(row, "registration_client_uri"),
            "issued_at": field(row, "issued_at") or datetime.now(timezone.utc),
        }
        if row is None:
            return await create_handler_record(ClientRegistration, db, payload)
        return await update_handler_record(ClientRegistration, db, record_id(row), payload)


get_client_registration = lambda client_id: run_async(get_client_registration_async(client_id))
upsert_client_registration = lambda **kwargs: run_async(upsert_client_registration_async(**kwargs))


__all__ = [
    "get_client_registration",
    "get_client_registration_async",
    "upsert_client_registration",
    "upsert_client_registration_async",
]

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx
from . import _table as _table_module

for _table_name in dir(_table_module):
    if not _table_name.startswith("__"):
        globals().setdefault(_table_name, getattr(_table_module, _table_name))

async def _read_registration(cls, db: Any, *, client_id: UUID) -> "ClientRegistration | None":
    return await first_record(cls, db, {"client_id": client_id})

@_table_op_ctx(bind=ClientRegistration, alias="update_registration", target="custom", rest=False)
async def update_registration(cls, db: Any, *, client_id: UUID, **payload: Any) -> "ClientRegistration | None":
    row = await _read_registration(cls, db, client_id=client_id)
    if row is None:
        return None
    return await update_record(cls, db, record_id(row), payload)

@_table_op_ctx(bind=ClientRegistration, alias="delete_registration", target="custom", rest=False)
async def delete_registration(cls, db: Any, *, client_id: UUID) -> Any:
    row = await _read_registration(cls, db, client_id=client_id)
    if row is None:
        return None
    return await delete_record(cls, db, record_id(row))

# END classmethod-to-op_ctx migration
