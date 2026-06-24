from __future__ import annotations

__all__: list[str] = []

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx

import uuid
from .._ops import create_record, field, first_record, list_records, read_record, record_id, update_record, utc_now
from ._table import CryptoKey
from ._usage import stored_key_operations, stored_key_usages
from typing import Any

async def _lookup_by_kid(cls, db: Any, *, kid: str, tenant_id: uuid.UUID | None = None) -> "CryptoKey | None":
    filters: dict[str, Any] = {"kid": kid}
    if tenant_id is not None:
        filters["tenant_id"] = tenant_id
    return await first_record(cls, db, filters)

@_table_op_ctx(bind=CryptoKey, alias="list_active", target="custom", rest=False)
async def list_active(
    cls,
    db: Any,
    *,
    tenant_id: uuid.UUID | None = None,
    key_usage: str | None = None,
    operation: str | None = None,
) -> list["CryptoKey"]:
    filters: dict[str, Any] = {"status": "active"}
    if tenant_id is not None:
        filters["tenant_id"] = tenant_id
    rows = await list_records(cls, db, filters)
    if key_usage is not None:
        rows = [row for row in rows if key_usage in set(field(row, "key_usages", []) or [])]
    if operation is not None:
        rows = [row for row in rows if operation in set(field(row, "allowed_ops", []) or [])]
    return rows

@_table_op_ctx(bind=CryptoKey, alias="retire", target="custom", rest=False)
async def retire(cls, db: Any, *, id: Any) -> "CryptoKey":
    row = await read_record(cls, db, id)
    metadata = dict(field(row, "key_metadata", {}) or {}) if row is not None else {}
    metadata["retired_at"] = utc_now().isoformat()
    return await update_record(cls, db, id, {"status": "retired", "key_metadata": metadata})

@_table_op_ctx(bind=CryptoKey, alias="rotate_record", target="custom", rest=False)
async def rotate_record(
    cls,
    db: Any,
    *,
    id: Any | None = None,
    kid: str | None = None,
    public_material: dict | str | None = None,
    public_material_format: str | None = None,
    provider_key_ref: str | None = None,
    provider: str | None = None,
    allowed_ops: Any = None,
    actor_user_id: uuid.UUID | None = None,
    actor_client_id: uuid.UUID | None = None,
    details: dict | None = None,
) -> "CryptoKey":
    from ..crypto_key_version import CryptoKeyVersion
    from ..key_rotation_event import KeyRotationEvent

    row = await read_record(cls, db, id) if id is not None else None
    if row is None and kid is not None:
        row = await _lookup_by_kid(cls, db, kid=kid)
    if row is None:
        raise LookupError("crypto key not found")

    next_version = int(field(row, "primary_version", 0) or 0) + 1
    await CryptoKeyVersion.create_version(
        db,
        key_id=record_id(row),
        version=next_version,
        status="active",
        public_material=public_material,
        public_material_format=public_material_format or field(row, "public_material_format"),
        provider_key_ref=provider_key_ref,
        provider=provider or field(row, "provider"),
        allowed_ops=stored_key_operations(
            key_kind=field(row, "key_kind"),
            key_usages=field(row, "key_usages"),
            allowed_ops=allowed_ops if allowed_ops is not None else field(row, "allowed_ops"),
        ),
    )
    next_allowed_ops = stored_key_operations(
        key_kind=field(row, "key_kind"),
        key_usages=field(row, "key_usages"),
        allowed_ops=allowed_ops if allowed_ops is not None else field(row, "allowed_ops"),
    )
    updated = await update_record(
        cls,
        db,
        record_id(row),
        {
            "primary_version": next_version,
            "public_material": public_material or field(row, "public_material"),
            "public_material_format": public_material_format or field(row, "public_material_format"),
            "provider_key_ref": provider_key_ref or field(row, "provider_key_ref"),
            "provider": provider or field(row, "provider"),
            "key_usages": stored_key_usages(field(row, "key_usages")),
            "allowed_ops": next_allowed_ops,
        },
    )
    await create_record(
        KeyRotationEvent,
        db,
        {
            "key_kid": field(row, "kid"),
            "algorithm": field(row, "algorithm"),
            "tenant_id": field(row, "tenant_id"),
            "actor_user_id": actor_user_id,
            "actor_client_id": actor_client_id,
            "details": {"version": next_version, **(details or {})},
            "event_type": "rotation",
        },
    )
    return updated

# END classmethod-to-op_ctx migration
