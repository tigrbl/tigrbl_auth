from __future__ import annotations

__all__: list[str] = []

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx
from . import _table as _table_module

for _table_name in dir(_table_module):
    if not _table_name.startswith("__"):
        globals().setdefault(_table_name, getattr(_table_module, _table_name))

@_table_op_ctx(bind=DeviceCode, alias="approve", target="custom", rest=False)
async def approve(
    cls,
    db: Any,
    *,
    user_id: uuid.UUID,
    user_code: str | None = None,
    device_code: str | None = None,
    id: Any | None = None,
    tenant_id: uuid.UUID | None = None,
) -> "DeviceCode | None":
    row = await read_record(cls, db, id) if id is not None else None
    if row is None:
        lookup_code = device_code or (str(id) if id is not None else None)
        row = await first_record(cls, db, {"device_code": lookup_code} if lookup_code else {"user_code": user_code})
    if row is None:
        return None
    return await update_record(
        cls,
        db,
        record_id(row),
        {
            "authorized": True,
            "authorized_at": utc_now(),
            "user_id": user_id,
            "tenant_id": tenant_id or field(row, "tenant_id"),
            "last_polled_at": None,
        },
    )

@_table_op_ctx(bind=DeviceCode, alias="deny", target="custom", rest=False)
async def deny(
    cls,
    db: Any,
    *,
    user_code: str | None = None,
    device_code: str | None = None,
    id: Any | None = None,
    reason: str | None = None,
) -> "DeviceCode | None":
    row = await read_record(cls, db, id) if id is not None else None
    if row is None:
        lookup_code = device_code or (str(id) if id is not None else None)
        row = await first_record(cls, db, {"device_code": lookup_code} if lookup_code else {"user_code": user_code})
    if row is None:
        return None
    return await update_record(cls, db, record_id(row), {"denied_at": utc_now(), "denial_reason": reason})

@_table_op_ctx(bind=DeviceCode, alias="poll", target="custom", rest=False)
async def poll(cls, db: Any, *, device_code: str) -> "DeviceCode | None":
    row = await first_record(cls, db, {"device_code": device_code})
    if row is None:
        return None
    return await update_record(
        cls,
        db,
        record_id(row),
        {"poll_count": int(field(row, "poll_count", 0) or 0) + 1, "last_polled_at": utc_now()},
    )

@_table_op_ctx(bind=DeviceCode, alias="consume", target="custom", rest=False)
async def consume(cls, db: Any, *, device_code: str) -> "DeviceCode | None":
    row = await first_record(cls, db, {"device_code": device_code})
    if row is None:
        return None
    return await update_record(cls, db, record_id(row), {"consumed_at": utc_now()})

# END classmethod-to-op_ctx migration
