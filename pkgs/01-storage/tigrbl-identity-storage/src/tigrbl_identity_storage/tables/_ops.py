"""Shared plumbing for table-owned storage operations."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any, Iterable
from uuid import UUID

from tigrbl_identity_core.digests import token_hash as token_hash



def utc_now() -> datetime:
    return datetime.now(timezone.utc)


UUID_FILTER_KEYS = {
    "id",
    "tenant_id",
    "user_id",
    "client_id",
    "session_id",
    "service_identity_id",
    "logout_id",
    "consent_id",
    "grant_id",
    "parent_grant_id",
    "child_grant_id",
    "replaced_by_grant_id",
    "actor_user_id",
    "actor_client_id",
}


def coerce_uuid_value(value: Any) -> Any:
    if value in {None, "", False}:
        return value
    if isinstance(value, UUID):
        return value
    try:
        return UUID(str(value))
    except Exception:
        return value


def normalize_uuid_identifier(value: Any) -> Any:
    return coerce_uuid_value(value)


def normalize_uuid_filters(filters: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: coerce_uuid_value(value) if key in UUID_FILTER_KEYS else value
        for key, value in filters.items()
    }


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
    if value in {None, "", False}:
        return None
    if isinstance(value, datetime):
        return value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)
    if isinstance(value, (int, float)):
        try:
            return datetime.fromtimestamp(float(value), tz=timezone.utc)
        except Exception:
            return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return parsed if parsed.tzinfo is not None else parsed.replace(tzinfo=timezone.utc)
    except Exception:
        return None


def normalize_audience(value: Any) -> list[str] | None:
    if value in {None, "", False}:
        return None
    if isinstance(value, str):
        return [value]
    if isinstance(value, Iterable):
        return [str(item) for item in value if item not in {None, ""}]
    return [str(value)]


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
    filters = normalize_uuid_filters(filters or {})
    result = await model.handlers.list.core({"payload": {"filters": filters}, "db": db})
    return [row for row in normalize_items(result) if row_matches(row, filters)]


async def first_record(model: Any, db: Any, filters: Mapping[str, Any]) -> Any:
    rows = await list_records(model, db, filters)
    return rows[0] if rows else None


async def read_record(model: Any, db: Any, ident: Any) -> Any:
    ident = normalize_uuid_identifier(ident)
    return await model.handlers.read.core({"path_params": {"id": ident}, "db": db})


async def create_record(model: Any, db: Any, payload: Mapping[str, Any]) -> Any:
    return created_item(await model.handlers.create.core({"payload": dict(payload), "db": db}))


async def update_record(model: Any, db: Any, ident: Any, payload: Mapping[str, Any]) -> Any:
    ident = normalize_uuid_identifier(ident)
    return created_item(
        await model.handlers.update.core({"path_params": {"id": ident}, "payload": dict(payload), "db": db})
    )


async def delete_record(model: Any, db: Any, ident: Any) -> Any:
    ident = normalize_uuid_identifier(ident)
    return await model.handlers.delete.core({"path_params": {"id": ident}, "db": db})


async def clear_records(model: Any, db: Any, filters: Mapping[str, Any] | None = None) -> Any:
    return await model.handlers.clear.core({"payload": {"filters": normalize_uuid_filters(filters or {})}, "db": db})


list_items = normalize_items
matches_filters = row_matches
list_handler_records = list_records
first_handler_record = first_record
read_handler_record = read_record
create_handler_record = create_record
update_handler_record = update_record
delete_handler_record = delete_record
clear_handler_records = clear_records
