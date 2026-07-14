"""Carrier-neutral durable token-introspection compatibility adapters."""

from __future__ import annotations

from typing import Any

from .sync import run_async
from .token_lifecycle import (
    introspect_token_async,
    remove_token_record_async,
    reset_token_state,
    reset_token_state_async,
)
from .token_persistence import upsert_token_record_async


def register_token(
    token: str,
    claims: dict[str, Any] | None = None,
) -> str:
    payload = dict(claims or {})
    return run_async(
        upsert_token_record_async(
            token,
            payload,
            token_kind=payload.get("kind"),
        )
    )


async def register_token_async(
    token: str,
    claims: dict[str, Any] | None = None,
) -> str:
    payload = dict(claims or {})
    return await upsert_token_record_async(
        token,
        payload,
        token_kind=payload.get("kind"),
    )


def unregister_token(token: str) -> None:
    run_async(remove_token_record_async(token))


def introspect_token(token: str) -> dict[str, Any]:
    return run_async(introspect_token_async(token))


def reset_tokens() -> None:
    reset_token_state()


async def reset_tokens_async() -> None:
    await reset_token_state_async()


__all__ = [
    "introspect_token",
    "introspect_token_async",
    "register_token",
    "register_token_async",
    "reset_tokens",
    "reset_tokens_async",
    "unregister_token",
]
