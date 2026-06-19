"""Storage-owned DeviceCode lifecycle hooks."""

from __future__ import annotations

from typing import Any, Mapping

from tigrbl_identity_server.framework import hook_ctx

from ._table import DeviceCode

_TIGRBL_HOOK_STAGE_KEY = "".join(("pha", "se"))


@hook_ctx(**{"ops": "approve", _TIGRBL_HOOK_STAGE_KEY: "HANDLER"})
async def approve_device_code(ctx: Mapping[str, Any]) -> None:
    payload = ctx.get("payload") or {}
    db = ctx.get("db") or ctx.get("session")
    ident = payload.get("id") or payload.get("device_code")
    if ident is None:
        return
    await DeviceCode.approve(
        db,
        id=ident if payload.get("id") is not None else None,
        device_code=ident if payload.get("device_code") is not None else None,
        user_id=payload.get("sub"),
        tenant_id=payload.get("tid"),
    )


@hook_ctx(**{"ops": "deny", _TIGRBL_HOOK_STAGE_KEY: "HANDLER"})
async def deny_device_code(ctx: Mapping[str, Any]) -> None:
    payload = ctx.get("payload") or {}
    db = ctx.get("db") or ctx.get("session")
    ident = payload.get("id") or payload.get("device_code")
    if ident is None:
        return
    await DeviceCode.deny(
        db,
        id=ident if payload.get("id") is not None else None,
        device_code=ident if payload.get("device_code") is not None else None,
        reason=payload.get("reason") or "access_denied",
    )


__all__ = ["approve_device_code", "deny_device_code"]
