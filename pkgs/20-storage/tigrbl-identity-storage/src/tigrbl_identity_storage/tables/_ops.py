"""Shared plumbing for table-owned storage operations."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def normalize_items(result: Any) -> list[Any]:
    if isinstance(result, Mapping) and isinstance(result.get("items"), list):
        result = result["items"]
    elif hasattr(result, "items"):
        result = result.items
    if isinstance(result, list):
        return result
    if isinstance(result, tuple):
        return list(result)
    if result is None:
        return []
    return [result]


def created_item(result: Any) -> Any:
    if isinstance(result, Mapping):
        for key in ("item", "result", "data"):
            if key in result:
                return result[key]
    return result


def field(row: Any, key: str, default: Any = None) -> Any:
    if isinstance(row, Mapping):
        return row.get(key, default)
    return getattr(row, key, default)


def record_id(row: Any) -> Any:
    return field(row, "id")


def value_matches(actual: Any, expected: Any) -> bool:
    if actual == expected:
        return True
    if actual is None or expected is None:
        return False
    return str(actual) == str(expected)


def row_matches(row: Any, filters: Mapping[str, Any]) -> bool:
    return all(value_matches(field(row, key), value) for key, value in filters.items())


async def list_records(model: Any, db: Any, filters: Mapping[str, Any] | None = None) -> list[Any]:
    filters = dict(filters or {})
    result = await model.handlers.list.core({"payload": {"filters": filters}, "db": db})
    return [row for row in normalize_items(result) if row_matches(row, filters)]


async def first_record(model: Any, db: Any, filters: Mapping[str, Any]) -> Any:
    rows = await list_records(model, db, filters)
    return rows[0] if rows else None


async def read_record(model: Any, db: Any, ident: Any) -> Any:
    return await model.handlers.read.core({"path_params": {"id": ident}, "db": db})


async def create_record(model: Any, db: Any, payload: Mapping[str, Any]) -> Any:
    return created_item(await model.handlers.create.core({"payload": dict(payload), "db": db}))


async def update_record(model: Any, db: Any, ident: Any, payload: Mapping[str, Any]) -> Any:
    return created_item(
        await model.handlers.update.core({"path_params": {"id": ident}, "payload": dict(payload), "db": db})
    )


async def delete_record(model: Any, db: Any, ident: Any) -> Any:
    return await model.handlers.delete.core({"path_params": {"id": ident}, "db": db})


async def clear_records(model: Any, db: Any, filters: Mapping[str, Any] | None = None) -> Any:
    return await model.handlers.clear.core({"payload": {"filters": dict(filters or {})}, "db": db})

