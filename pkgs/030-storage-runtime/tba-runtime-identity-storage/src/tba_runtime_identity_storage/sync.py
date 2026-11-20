"""Synchronous compatibility bridge for layer-30 async lifecycle operations."""

from __future__ import annotations

import asyncio
from collections.abc import Coroutine
from typing import Any


def run_async(coro: Coroutine[Any, Any, Any]) -> Any:
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)
    coro.close()
    raise RuntimeError(
        "sync runtime helpers cannot run inside an active event loop; "
        "use the async lifecycle operation"
    )


__all__ = ["run_async"]
