"""Construct carrier-neutral operations for canonical durable tables."""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Mapping, Sequence
from typing import Any

from tigrbl import OpSpec

RuntimeStep = Callable[..., object | Awaitable[object]]


def makeRuntimeOperation(
    *,
    alias: str,
    handler: RuntimeStep,
    target: str = "custom",
    arity: str = "collection",
    tx_scope: str = "read_write",
    persist: str = "default",
    request_model: object | None = None,
    response_model: object | None = None,
    hooks: Sequence[object] = (),
    extra: Mapping[str, Any] | None = None,
) -> OpSpec:
    """Build one durable semantic operation without choosing a carrier."""

    if not alias or not alias.strip():
        raise ValueError("runtime operation alias is required")
    if not callable(handler):
        raise TypeError("runtime operation handler must be callable")
    return OpSpec(
        alias=alias,
        target=target,
        arity=arity,
        expose_routes=False,
        expose_rpc=False,
        expose_method=True,
        bindings=(),
        tx_scope=tx_scope,
        persist=persist,
        request_model=request_model,
        response_model=response_model,
        handler=handler,
        core=handler,
        core_raw=handler,
        hooks=tuple(hooks),
        extra={"owner_layer": "30-storage-runtime", **dict(extra or {})},
    )


runtime_operation = makeRuntimeOperation

__all__ = ["RuntimeStep", "makeRuntimeOperation", "runtime_operation"]
