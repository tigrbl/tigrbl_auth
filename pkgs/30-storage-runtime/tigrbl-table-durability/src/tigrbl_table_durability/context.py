"""Carrier-neutral extraction of table-operation execution context."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


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


__all__ = ["database_from_context", "payload_from_context"]
