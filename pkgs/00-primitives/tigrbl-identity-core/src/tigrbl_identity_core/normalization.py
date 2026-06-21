"""Normalization helpers shared by identity packages."""

from __future__ import annotations

from collections.abc import Iterable


def normal_tuple(values: Iterable[str] | None) -> tuple[str, ...]:
    """Return a sorted tuple of non-empty stripped string values."""

    return tuple(sorted({str(value).strip() for value in values or () if str(value).strip()}))


__all__ = ["normal_tuple"]
