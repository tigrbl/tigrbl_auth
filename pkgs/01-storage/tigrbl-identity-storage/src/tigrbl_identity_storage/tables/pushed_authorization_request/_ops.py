from __future__ import annotations

__all__: list[str] = []

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx
from . import _table as _table_module

for _table_name in dir(_table_module):
    if not _table_name.startswith("__"):
        globals().setdefault(_table_name, getattr(_table_module, _table_name))

@_table_op_ctx(bind=PushedAuthorizationRequest, alias="resolve_request_uri", target="custom", rest=False)
async def resolve_request_uri(
    cls,
    db: Any,
    *,
    request_uri: str,
    client_id: uuid.UUID | str | None = None,
) -> "PushedAuthorizationRequest | None":
    row = await first_record(cls, db, {"request_uri": request_uri})
    if row is None or row.is_expired() or row.is_consumed() or not row.client_bound(client_id):
        return None
    return row

@_table_op_ctx(bind=PushedAuthorizationRequest, alias="consume_request", target="custom", rest=False)
async def consume_request(cls, db: Any, *, request_uri: str) -> "PushedAuthorizationRequest | None":
    row = await first_record(cls, db, {"request_uri": request_uri})
    if row is None:
        return None
    return await update_record(cls, db, record_id(row), {"consumed_at": datetime.now(tz=timezone.utc)})

# END classmethod-to-op_ctx migration
