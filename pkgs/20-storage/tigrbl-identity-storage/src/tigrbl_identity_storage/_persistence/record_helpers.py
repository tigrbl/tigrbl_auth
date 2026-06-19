"""Shared handler-record helpers for storage persistence modules."""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Any, Mapping
from uuid import UUID

from .uuid_coercion import normalize_uuid_filters, normalize_uuid_identifier


def token_hash(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def to_uuid(value: Any) -> UUID | None:
    if value in {None, "", False}:
        return None
    if isinstance(value, UUID):
        return value
    try:
        return UUID(str(value))
    except Exception:
        return None


def to_datetime(value: Any) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)
    try:
        return datetime.fromtimestamp(int(value), tz=timezone.utc)
    except Exception:
        return None


def normalize_audience(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (str, dict, list)):
        return value
    if isinstance(value, tuple):
        return list(value)
    return str(value)


def created_item(value: Any) -> Any:
    if isinstance(value, Mapping):
        for key in ("item", "result", "data"):
            if key in value:
                return value[key]
    return value


def list_items(result: Any) -> list[Any]:
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


def matches_filters(row: Any, filters: Mapping[str, Any]) -> bool:
    return all(value_matches(field(row, key), expected) for key, expected in filters.items())


async def list_handler_records(model: Any, db: Any, filters: Mapping[str, Any] | None = None) -> list[Any]:
    filters = normalize_uuid_filters(filters or {})
    result = await model.handlers.list.core({"payload": {"filters": filters}, "db": db})
    return [row for row in list_items(result) if matches_filters(row, filters)]


async def first_handler_record(model: Any, db: Any, filters: Mapping[str, Any]) -> Any:
    rows = await list_handler_records(model, db, filters)
    return rows[0] if rows else None


async def read_handler_record(model: Any, db: Any, ident: Any) -> Any:
    return await model.handlers.read.core({"path_params": {"id": normalize_uuid_identifier(ident)}, "db": db})


async def create_handler_record(model: Any, db: Any, payload: Mapping[str, Any]) -> Any:
    return created_item(await model.handlers.create.core({"payload": dict(payload), "db": db}))


async def update_handler_record(model: Any, db: Any, ident: Any, payload: Mapping[str, Any]) -> Any:
    return created_item(
        await model.handlers.update.core(
            {"path_params": {"id": normalize_uuid_identifier(ident)}, "payload": dict(payload), "db": db}
        )
    )


async def delete_handler_record(model: Any, db: Any, ident: Any) -> Any:
    return await model.handlers.delete.core({"path_params": {"id": normalize_uuid_identifier(ident)}, "db": db})


async def clear_handler_records(model: Any, db: Any, filters: Mapping[str, Any] | None = None) -> Any:
    return await model.handlers.clear.core({"payload": {"filters": normalize_uuid_filters(filters or {})}, "db": db})
