"""Certified-core request principal context."""

from __future__ import annotations

import contextvars

principal_var: contextvars.ContextVar[dict | None] = contextvars.ContextVar(
    "principal", default=None
)

__all__ = ["principal_var"]
