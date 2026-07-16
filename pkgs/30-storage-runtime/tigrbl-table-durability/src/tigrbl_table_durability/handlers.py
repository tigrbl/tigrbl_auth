"""Invoke canonical Tigrbl table handlers through a supplied session."""

from __future__ import annotations

import inspect
from collections.abc import Awaitable, Callable, Mapping
from typing import Any
from uuid import UUID

from .context import database_from_context, payload_from_context

SENSITIVE_RAW_FIELDS = frozenset(
    {"raw_nonce", "pre_authorized_code", "presentation_disclosures", "raw_payload"}
)
UUID_FILTER_KEYS = frozenset(
    {
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
)


async def maybe_await(value: object | Awaitable[object]) -> object:
    if inspect.isawaitable(value):
        return await value
    return value


def field_value(row: Any, key: str, default: Any = None) -> Any:
    return (
        row.get(key, default)
        if isinstance(row, Mapping)
        else getattr(row, key, default)
    )


def record_identifier(row: Any) -> Any:
    return field_value(row, "id")


def normalize_identifier(value: Any) -> Any:
    if value in {None, "", False} or isinstance(value, UUID):
        return value
    try:
        return UUID(str(value))
    except (TypeError, ValueError, AttributeError):
        return value


coerce_uuid_value = normalize_identifier
normalize_uuid_identifier = normalize_identifier


def normalize_uuid_filters(filters: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: normalize_identifier(value) if key in UUID_FILTER_KEYS else value
        for key, value in filters.items()
    }


def normalize_items(result: Any) -> list[Any]:
    if isinstance(result, Mapping):
        result = result.get("items", result.get("data", result))
    elif hasattr(result, "items") and not isinstance(result, (list, tuple)):
        result = result.items
    if result is None:
        return []
    if isinstance(result, list):
        return result
    if isinstance(result, tuple):
        return list(result)
    return [result]


async def list_table_records(
    table: type,
    db: Any,
    filters: Mapping[str, Any] | None = None,
) -> list[Any]:
    filters = normalize_uuid_filters(filters or {})
    context = {"payload": {"filters": filters}, "db": db}
    core = table.handlers.list.core
    if "model" in inspect.signature(core, follow_wrapped=False).parameters:
        result = await maybe_await(core(table, filters=filters, db=db))
    else:
        result = await maybe_await(core(context))
    return [
        row
        for row in normalize_items(result)
        if all(
            str(field_value(row, key)) == str(value) for key, value in filters.items()
        )
    ]


async def first_table_record(table: type, db: Any, filters: Mapping[str, Any]) -> Any:
    rows = await list_table_records(table, db, filters)
    return rows[0] if rows else None


def reject_sensitive_raw_fields(payload: Mapping[str, Any]) -> None:
    forbidden = SENSITIVE_RAW_FIELDS.intersection(payload)
    if forbidden:
        raise ValueError(
            "sensitive raw fields must not be persisted: "
            + ", ".join(sorted(forbidden))
        )


async def _call(
    core: Callable[..., object],
    table: type,
    db: Any,
    context: Mapping[str, Any],
    *args: Any,
) -> object:
    if "model" in inspect.signature(core, follow_wrapped=False).parameters:
        return await maybe_await(core(table, *args, db))
    return await maybe_await(core(dict(context)))


async def create_table_record(table: type, db: Any, payload: Mapping[str, Any]) -> Any:
    context = {"payload": dict(payload), "db": db}
    result = await _call(table.handlers.create.core, table, db, context, dict(payload))
    return result.get("item", result) if isinstance(result, Mapping) else result


async def read_table_record(table: type, db: Any, ident: Any) -> Any:
    ident = normalize_identifier(ident)
    return await _call(
        table.handlers.read.core,
        table,
        db,
        {"path_params": {"id": ident}, "db": db},
        ident,
    )


async def update_table_record(
    table: type, db: Any, ident: Any, payload: Mapping[str, Any]
) -> Any:
    ident = normalize_identifier(ident)
    context = {"path_params": {"id": ident}, "payload": dict(payload), "db": db}
    result = await _call(
        table.handlers.update.core, table, db, context, ident, dict(payload)
    )
    return result.get("item", result) if isinstance(result, Mapping) else result


async def delete_table_record(table: type, db: Any, ident: Any) -> Any:
    ident = normalize_identifier(ident)
    return await _call(
        table.handlers.delete.core,
        table,
        db,
        {"path_params": {"id": ident}, "db": db},
        ident,
    )


async def clear_table_records(
    table: type,
    db: Any,
    filters: Mapping[str, Any] | None = None,
) -> object:
    filters = normalize_uuid_filters(filters or {})
    context = {"payload": {"filters": filters}, "db": db}
    core = table.handlers.clear.core
    if "model" in inspect.signature(core, follow_wrapped=False).parameters:
        return await maybe_await(core(table, filters=filters, db=db))
    return await maybe_await(core(context))


def create_table_handler(
    table: type, *, reject_sensitive: bool = True
) -> Callable[[Mapping[str, Any]], Awaitable[object]]:
    async def create(ctx: Mapping[str, Any]) -> object:
        payload = payload_from_context(ctx)
        if reject_sensitive:
            reject_sensitive_raw_fields(payload)
        return await create_table_record(table, database_from_context(ctx), payload)

    create.__name__ = f"create_{table.__name__}"
    return create


field = field_value
record_id = record_identifier
create_record = create_handler_record = create_table_record
read_record = read_handler_record = read_table_record
update_record = update_handler_record = update_table_record
delete_record = delete_handler_record = delete_table_record
list_records = list_handler_records = list_table_records
first_record = first_handler_record = first_table_record
clear_records = clear_handler_records = clear_table_records


__all__ = [
    "SENSITIVE_RAW_FIELDS",
    "UUID_FILTER_KEYS",
    "clear_table_records",
    "clear_handler_records",
    "clear_records",
    "coerce_uuid_value",
    "create_handler_record",
    "create_record",
    "create_table_handler",
    "create_table_record",
    "database_from_context",
    "delete_table_record",
    "delete_handler_record",
    "delete_record",
    "field",
    "field_value",
    "first_table_record",
    "first_handler_record",
    "first_record",
    "list_table_records",
    "list_handler_records",
    "list_records",
    "maybe_await",
    "normalize_identifier",
    "normalize_uuid_filters",
    "normalize_uuid_identifier",
    "normalize_items",
    "payload_from_context",
    "read_table_record",
    "read_handler_record",
    "read_record",
    "record_id",
    "record_identifier",
    "reject_sensitive_raw_fields",
    "update_table_record",
    "update_handler_record",
    "update_record",
]
