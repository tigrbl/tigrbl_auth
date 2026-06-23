"""Table-owned operator store metadata."""

from __future__ import annotations

import json
from typing import Any

from tigrbl_identity_storage.framework import RestOltpTable, Mapped, S, String, TZDateTime, acol

from .._ops import create_record, field, first_record, list_records, record_id, update_record, utc_now


class OperatorMetadata(RestOltpTable):
    __tablename__ = "operator_metadata"

    key: Mapped[str] = acol(storage=S(String(255), primary_key=True, nullable=False))
    value_json: Mapped[str] = acol(storage=S(String(8000), nullable=False, default="null"))
    updated_at: Mapped[Any] = acol(storage=S(TZDateTime, nullable=False, default=utc_now))

    @classmethod
    async def upsert_metadata(cls, db: Any, key: str, value: Any) -> "OperatorMetadata":
        row = await first_record(cls, db, {"key": key})
        payload = {"key": key, "value_json": json.dumps(value, sort_keys=True), "updated_at": utc_now()}
        if row is None:
            return await create_record(cls, db, payload)
        return await update_record(cls, db, record_id(row) or key, payload)

    @classmethod
    async def load_metadata(cls, db: Any) -> dict[str, Any]:
        rows = await list_records(cls, db)
        loaded: dict[str, Any] = {}
        for row in rows:
            try:
                loaded[str(field(row, "key"))] = json.loads(field(row, "value_json") or "null")
            except Exception:
                loaded[str(field(row, "key"))] = None
        return loaded


__all__ = ["OperatorMetadata"]
