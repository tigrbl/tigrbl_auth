"""Runtime enforcement helpers for storage-backed crypto operations."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


def _row_value(row: Any, key: str, default: Any = None) -> Any:
    if isinstance(row, Mapping):
        return row.get(key, default)
    return getattr(row, key, default)


def _string_set(values: Any) -> set[str]:
    if values is None or values == "" or values is False:
        return set()
    if isinstance(values, str):
        return {values}
    return {str(value) for value in values if value not in {None, ""}}


def ensure_allowed_op(row: Any, operation: str) -> None:
    if str(_row_value(row, "status", "")) != "active":
        raise LookupError("active crypto key not found")
    allowed = _string_set(_row_value(row, "allowed_ops"))
    if str(operation) not in allowed:
        kid = _row_value(row, "kid", "<unknown>")
        raise PermissionError(f"crypto key {kid} is not allowed to perform {operation}")


def provider_key_ref_from_row(row: Any) -> Any:
    ref = _row_value(row, "provider_key_ref")
    if ref is None or ref == "":
        raise LookupError("crypto key provider reference is not available")
    return ref


def public_material_from_row(row: Any) -> Any:
    material = _row_value(row, "public_material")
    if material is None or material == "":
        raise LookupError("crypto key public material is not available")
    return material


__all__ = ["ensure_allowed_op", "provider_key_ref_from_row", "public_material_from_row"]
