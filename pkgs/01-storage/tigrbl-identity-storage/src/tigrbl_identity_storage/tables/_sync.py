"""Synchronous compatibility wrapper for table-owned async helpers."""

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
    raise RuntimeError("sync table helpers cannot run inside an active event loop; use the async helper")


__all__ = ["run_async"]
