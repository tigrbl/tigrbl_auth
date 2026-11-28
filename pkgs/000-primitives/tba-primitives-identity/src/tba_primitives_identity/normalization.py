"""Normalization helpers shared by identity packages."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any
from uuid import uuid4


def new_model_id() -> str:
    """Return a dependency-light opaque identifier for concrete models."""

    return str(uuid4())


def required_text(value: object, field_name: str) -> str:
    """Normalize a required textual field."""

    cleaned = str(value).strip()
    if not cleaned:
        raise ValueError(f"{field_name} is required")
    return cleaned


def clean_tuple(values: Iterable[object] = ()) -> tuple[str, ...]:
    """Return unique, non-empty textual values in stable order."""

    return tuple(sorted({str(value).strip() for value in values if str(value).strip()}))


def clean_mapping(value: Mapping[str, Any], field_name: str) -> dict[str, Any]:
    """Validate and copy a mapping owned by a concrete model."""

    if not isinstance(value, Mapping):
        raise ValueError(f"{field_name} must be a mapping")
    return dict(value)


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


__all__ = [
    "clean_mapping",
    "clean_tuple",
    "new_model_id",
    "normal_tuple",
    "pick_fields",
    "required_text",
    "row_active",
    "row_value",
    "str_tuple",
]
