from __future__ import annotations

__all__: list[str] = []

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx

import datetime as dt
from .._ops import create_record, field, record_id, update_record, utc_now
from ._table import Credential
from typing import Any

async def _create_credential(
    cls,
    db: Any,
    *,
    principal_id: str,
    credential_kind: str,
    secret_digest: str | None = None,
    public_id: str | None = None,
    status: str = "active",
    version: int = 1,
    rotated_from: str | None = None,
    expires_at: dt.datetime | None = None,
    credential_metadata: dict | None = None,
) -> "Credential":
    return await create_record(
        cls,
        db,
        {
            "principal_id": principal_id,
            "credential_kind": credential_kind,
            "secret_digest": secret_digest,
            "public_id": public_id,
            "status": status,
            "version": version,
            "rotated_from": rotated_from,
            "expires_at": expires_at,
            "credential_metadata": credential_metadata,
        },
    )

@_table_op_ctx(bind=Credential, alias="rotate", target="custom", rest=False)
async def rotate(
    cls,
    db: Any,
    *,
    id: Any,
    secret_digest: str | None = None,
    public_id: str | None = None,
    credential_metadata: dict | None = None,
) -> "Credential":
    row = await update_record(cls, db, id, {"status": "rotated"})
    return await _create_credential(cls,
        db,
        principal_id=field(row, "principal_id"),
        credential_kind=field(row, "credential_kind"),
        secret_digest=secret_digest,
        public_id=public_id,
        version=int(field(row, "version", 1) or 1) + 1,
        rotated_from=str(record_id(row)),
        credential_metadata=credential_metadata,
    )

@_table_op_ctx(bind=Credential, alias="revoke", target="custom", rest=False)
async def revoke(cls, db: Any, *, id: Any, reason: str | None = None) -> "Credential":
    meta = {"revoked_at": utc_now().isoformat()}
    if reason:
        meta["revoked_reason"] = reason
    return await update_record(cls, db, id, {"status": "revoked", "credential_metadata": meta})

# END classmethod-to-op_ctx migration
