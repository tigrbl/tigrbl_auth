from __future__ import annotations

__all__: list[str] = []

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx
from . import _table as _table_module

for _table_name in dir(_table_module):
    if not _table_name.startswith("__"):
        globals().setdefault(_table_name, getattr(_table_module, _table_name))

@_table_op_ctx(bind=CryptoKeyVersion, alias="create_version", target="custom", rest=False)
async def create_version(
    cls,
    db: Any,
    *,
    key_id: uuid.UUID,
    version: int,
    status: str = "active",
    public_material: dict | str | None = None,
    public_material_format: str | None = None,
    provider_key_ref: str | None = None,
    provider: str | None = None,
    allowed_ops: Any = None,
    fingerprint: str | None = None,
    not_before: dt.datetime | None = None,
    not_after: dt.datetime | None = None,
    activated_at: dt.datetime | None = None,
    retired_at: dt.datetime | None = None,
    version_metadata: dict | None = None,
) -> "CryptoKeyVersion":
    existing = await _lookup(cls, db, key_id=key_id, version=version)
    payload = {
        "key_id": key_id,
        "version": version,
        "status": status,
        "public_material": public_material,
        "public_material_format": public_material_format,
        "provider_key_ref": provider_key_ref,
        "provider": provider,
        "allowed_ops": _operation_list(allowed_ops),
        "fingerprint": fingerprint,
        "not_before": not_before,
        "not_after": not_after,
        "activated_at": activated_at,
        "retired_at": retired_at,
        "version_metadata": version_metadata,
    }
    if existing is not None:
        return await update_record(cls, db, record_id(existing), payload)
    return await create_record(cls, db, payload)

async def _lookup(cls, db: Any, *, key_id: uuid.UUID, version: int) -> "CryptoKeyVersion | None":
    return await first_record(cls, db, {"key_id": key_id, "version": version})

@_table_op_ctx(bind=CryptoKeyVersion, alias="activate", target="custom", rest=False)
async def activate(cls, db: Any, *, key_id: uuid.UUID, version: int) -> "CryptoKeyVersion | None":
    row = await _lookup(cls, db, key_id=key_id, version=version)
    if row is None:
        return None
    return await update_record(
        cls,
        db,
        record_id(row),
        {"status": "active", "activated_at": utc_now(), "retired_at": None},
    )

@_table_op_ctx(bind=CryptoKeyVersion, alias="retire", target="custom", rest=False)
async def retire(cls, db: Any, *, key_id: uuid.UUID, version: int) -> "CryptoKeyVersion | None":
    row = await _lookup(cls, db, key_id=key_id, version=version)
    if row is None:
        return None
    version_metadata = dict(getattr(row, "version_metadata", None) or {})
    retired_at = utc_now()
    version_metadata["retired_at"] = retired_at.isoformat()
    return await update_record(
        cls,
        db,
        record_id(row),
        {"status": "retired", "retired_at": retired_at, "version_metadata": version_metadata},
    )

@_table_op_ctx(bind=CryptoKeyVersion, alias="export_public_material", target="custom", rest=False)
async def export_public_material(cls, db: Any, *, key_id: uuid.UUID, version: int) -> dict[str, Any] | str | None:
    row = await _lookup(cls, db, key_id=key_id, version=version)
    material = getattr(row, "public_material", None) if row is not None else None
    if isinstance(material, dict):
        return {key: value for key, value in material.items() if key not in {"d", "p", "q", "dp", "dq", "qi"}}
    return material if isinstance(material, str) else None

# END classmethod-to-op_ctx migration
