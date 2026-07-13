"""Shared execution helpers for canonical Tigrbl table handlers."""

from __future__ import annotations

import inspect
from collections.abc import Awaitable, Callable, Mapping
from typing import Any


SENSITIVE_RAW_FIELDS = frozenset(
    {"raw_nonce", "pre_authorized_code", "presentation_disclosures", "raw_payload"}
)


def payload_from_context(ctx: Mapping[str, Any]) -> Mapping[str, Any]:
    payload = ctx.get("payload", ctx.get("data", {}))
    if not isinstance(payload, Mapping):
        raise TypeError("runtime operation payload must be a mapping")
    return payload


def database_from_context(ctx: Mapping[str, Any]) -> Any:
    try:
        return ctx["db"]
    except KeyError as exc:
        raise ValueError("runtime operation requires a database session") from exc


def reject_sensitive_raw_fields(payload: Mapping[str, Any]) -> None:
    forbidden = SENSITIVE_RAW_FIELDS.intersection(payload)
    if forbidden:
        names = ", ".join(sorted(forbidden))
        raise ValueError(f"sensitive raw fields must not be persisted: {names}")


async def maybe_await(value: object | Awaitable[object]) -> object:
    if inspect.isawaitable(value):
        return await value
    return value


async def _call_table_core(
    core: Callable[..., object],
    *,
    table: type,
    db: Any,
    context: Mapping[str, Any],
    positional: tuple[Any, ...],
) -> object:
    """Call production Tigrbl cores and context-shaped test/runtime adapters."""

    parameters = inspect.signature(core).parameters
    if "model" in parameters:
        return await maybe_await(core(table, *positional, db))
    return await maybe_await(core(dict(context)))


def field_value(row: Any, key: str, default: Any = None) -> Any:
    if isinstance(row, Mapping):
        return row.get(key, default)
    return getattr(row, key, default)


def record_identifier(row: Any) -> Any:
    return field_value(row, "id")


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
    filters = dict(filters or {})
    context = {"payload": {"filters": filters}, "db": db}
    core = table.handlers.list.core
    parameters = inspect.signature(core).parameters
    if "model" in parameters:
        result = await maybe_await(core(table, filters=filters, db=db))
    else:
        result = await maybe_await(core(context))
    return [
        row
        for row in normalize_items(result)
        if all(str(field_value(row, key)) == str(value) for key, value in filters.items())
    ]


async def first_table_record(
    table: type,
    db: Any,
    filters: Mapping[str, Any],
) -> Any:
    rows = await list_table_records(table, db, filters)
    return rows[0] if rows else None


async def create_table_record(
    table: type,
    db: Any,
    payload: Mapping[str, Any],
) -> Any:
    context = {"payload": dict(payload), "db": db}
    result = await _call_table_core(
        table.handlers.create.core,
        table=table,
        db=db,
        context=context,
        positional=(dict(payload),),
    )
    return result.get("item", result) if isinstance(result, Mapping) else result


async def update_table_record(
    table: type,
    db: Any,
    identifier: Any,
    payload: Mapping[str, Any],
) -> Any:
    context = {
        "path_params": {"id": identifier},
        "payload": dict(payload),
        "db": db,
    }
    result = await _call_table_core(
        table.handlers.update.core,
        table=table,
        db=db,
        context=context,
        positional=(identifier, dict(payload)),
    )
    return result.get("item", result) if isinstance(result, Mapping) else result


async def delete_table_record(table: type, db: Any, identifier: Any) -> Any:
    context = {"path_params": {"id": identifier}, "db": db}
    return await _call_table_core(
        table.handlers.delete.core,
        table=table,
        db=db,
        context=context,
        positional=(identifier,),
    )


async def clear_table_records(
    table: type,
    db: Any,
    filters: Mapping[str, Any] | None = None,
) -> object:
    filters = dict(filters or {})
    context = {"payload": {"filters": filters}, "db": db}
    core = table.handlers.clear.core
    parameters = inspect.signature(core).parameters
    if "model" in parameters:
        return await maybe_await(core(table, filters=filters, db=db))
    return await maybe_await(core(context))


def create_table_handler(
    table: type,
    *,
    reject_sensitive: bool = True,
) -> Callable[[Mapping[str, Any]], Awaitable[object]]:
    """Create through the canonical table handler using the caller's session."""

    async def create(ctx: Mapping[str, Any]) -> object:
        payload = payload_from_context(ctx)
        if reject_sensitive:
            reject_sensitive_raw_fields(payload)
        return await maybe_await(
            table.handlers.create.core(table, payload, database_from_context(ctx))
        )

    create.__name__ = f"create_{table.__name__}"
    return create


__all__ = [
    "SENSITIVE_RAW_FIELDS",
    "clear_table_records",
    "create_table_handler",
    "create_table_record",
    "database_from_context",
    "delete_table_record",
    "field_value",
    "first_table_record",
    "list_table_records",
    "maybe_await",
    "payload_from_context",
    "record_identifier",
    "reject_sensitive_raw_fields",
    "update_table_record",
]
