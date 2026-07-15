"""Injected durable-state adapters for DPoP nonce and replay operations."""

from __future__ import annotations

import inspect
from typing import Any

from .primitives import _ALLOWED_SKEW


def _require_callable(fn: Any | None, purpose: str) -> Any:
    if not callable(fn):
        raise RuntimeError(
            f"{purpose} requires an injected DPoP table-backed operation"
        )
    return fn


async def _maybe_await(value: Any) -> Any:
    if inspect.isawaitable(value):
        return await value
    return value


def issue_nonce(*, ttl_s: int = _ALLOWED_SKEW, issuer: Any | None = None) -> str:
    return _require_callable(issuer, "issue_nonce")(ttl_s=ttl_s)


async def issue_nonce_async(
    *, ttl_s: int = _ALLOWED_SKEW, issuer: Any | None = None
) -> str:
    return await _maybe_await(
        _require_callable(issuer, "issue_nonce_async")(ttl_s=ttl_s)
    )


def register_nonce(
    nonce: str, *, ttl_s: int = _ALLOWED_SKEW, registrar: Any | None = None
) -> str:
    return _require_callable(registrar, "register_nonce")(nonce, ttl_s=ttl_s)


async def register_nonce_async(
    nonce: str, *, ttl_s: int = _ALLOWED_SKEW, registrar: Any | None = None
) -> str:
    return await _maybe_await(
        _require_callable(registrar, "register_nonce_async")(nonce, ttl_s=ttl_s)
    )


def consume_nonce(
    nonce: str, *, consumer: Any | None = None, now: int | None = None
) -> bool:
    return _require_callable(consumer, "consume_nonce")(nonce, now=now)


async def consume_nonce_async(
    nonce: str, *, consumer: Any | None = None, now: int | None = None
) -> bool:
    return await _maybe_await(
        _require_callable(consumer, "consume_nonce_async")(nonce, now=now)
    )


def replay_table_snapshot(snapshotter: Any | None = None) -> dict[str, int]:
    return _require_callable(snapshotter, "replay_table_snapshot")()


async def replay_table_snapshot_async(
    snapshotter: Any | None = None,
) -> dict[str, int]:
    return await _maybe_await(
        _require_callable(snapshotter, "replay_table_snapshot_async")()
    )
