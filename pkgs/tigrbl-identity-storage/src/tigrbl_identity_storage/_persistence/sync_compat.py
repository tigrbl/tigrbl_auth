"""Synchronous compatibility wrappers for async persistence helpers."""

from __future__ import annotations

import asyncio
from collections.abc import Coroutine
from typing import Any


def _run(coro: Coroutine[Any, Any, Any]) -> Any:
    """Run an async persistence helper from a true synchronous caller.

    Calling this from an active event loop would block the loop or require a
    second thread-local loop. That is not a valid request/runtime path; async
    callers must use the async helper directly.
    """

    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)
    coro.close()
    raise RuntimeError("sync persistence helpers cannot run inside an active event loop; use the async helper")
