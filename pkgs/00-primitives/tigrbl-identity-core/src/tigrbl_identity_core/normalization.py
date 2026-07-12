"""Normalization helpers shared by identity packages."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any


def pick_fields(record: Mapping[str, Any], fields: Iterable[str]) -> dict[str, Any]:
    return {field: record[field] for field in fields if field in record}


def row_value(row: Any, key: str, default: Any = None) -> Any:
    if isinstance(row, Mapping):
        return row.get(key, default)
    return getattr(row, key, default)


def row_active(row: Any) -> bool:
    return str(row_value(row, "status", "active") or "active") == "active"


def str_tuple(values: Any, *, sort: bool = True) -> tuple[str, ...]:
    if values is None or values == "" or values is False:
        return ()
    if isinstance(values, str):
        items = (values,)
    else:
        items = tuple(str(value) for value in values if value not in {None, ""})
    return tuple(sorted(set(items))) if sort else tuple(items)


def normal_tuple(values: Iterable[str] | None) -> tuple[str, ...]:
    """Return a sorted tuple of non-empty stripped string values."""

    return tuple(
        sorted({str(value).strip() for value in values or () if str(value).strip()})
    )


__all__ = ["normal_tuple", "pick_fields", "row_active", "row_value", "str_tuple"]
