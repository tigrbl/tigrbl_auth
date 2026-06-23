from __future__ import annotations

from typing import Any


def normalize_refresh_audience(value: Any) -> str | list[str] | None:
    if value is None or value == "":
        return None
    if isinstance(value, (str, list)):
        return value
    if isinstance(value, tuple):
        return list(value)
    return str(value)


__all__ = ["normalize_refresh_audience"]
