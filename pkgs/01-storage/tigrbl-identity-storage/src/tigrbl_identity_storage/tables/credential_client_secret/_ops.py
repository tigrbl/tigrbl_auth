from __future__ import annotations

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx

from .._ops import first_record, record_id, update_record
from ._table import CredentialClientSecret
from typing import Any

@_table_op_ctx(bind=CredentialClientSecret, alias="revoke", target="custom", rest=False)
async def revoke(cls, db: Any, *, credential_id: str) -> "CredentialClientSecret | None":
    row = await first_record(cls, db, {"credential_id": credential_id})
    if row is None:
        return None
    return await update_record(cls, db, record_id(row), {"status": "revoked"})

# END classmethod-to-op_ctx migration
