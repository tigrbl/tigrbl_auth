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
    "create_table_handler",
    "database_from_context",
    "maybe_await",
    "payload_from_context",
    "reject_sensitive_raw_fields",
]
