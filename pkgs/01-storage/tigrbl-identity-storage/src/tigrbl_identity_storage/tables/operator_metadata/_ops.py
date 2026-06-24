from __future__ import annotations

__all__: list[str] = []

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx
from . import _table as _table_module

for _table_name in dir(_table_module):
    if not _table_name.startswith("__"):
        globals().setdefault(_table_name, getattr(_table_module, _table_name))

@_table_op_ctx(bind=OperatorMetadata, alias="upsert_metadata", target="custom", rest=False)
async def upsert_metadata(cls, db: Any, key: str, value: Any) -> "OperatorMetadata":
    row = await first_record(cls, db, {"key": key})
    payload = {"key": key, "value_json": json.dumps(value, sort_keys=True), "updated_at": utc_now()}
    if row is None:
        return await create_record(cls, db, payload)
    return await update_record(cls, db, record_id(row) or key, payload)

@_table_op_ctx(bind=OperatorMetadata, alias="load_metadata", target="custom", rest=False)
async def load_metadata(cls, db: Any) -> dict[str, Any]:
    rows = await list_records(cls, db)
    loaded: dict[str, Any] = {}
    for row in rows:
        try:
            loaded[str(field(row, "key"))] = json.loads(field(row, "value_json") or "null")
        except Exception:
            loaded[str(field(row, "key"))] = None
    return loaded

# END classmethod-to-op_ctx migration
