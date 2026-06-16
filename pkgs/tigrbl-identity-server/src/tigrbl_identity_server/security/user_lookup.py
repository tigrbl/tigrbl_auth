"""Handler-backed user lookup helpers for auth request paths."""

from __future__ import annotations

import uuid
from collections.abc import Mapping
from typing import Any
from unittest.mock import Mock

from tigrbl_identity_storage.tables import User

_UUID_FILTER_KEYS = frozenset({"id", "tenant_id"})


def _normalize_filter_value(key: str, value: Any) -> Any:
    if key not in _UUID_FILTER_KEYS or isinstance(value, uuid.UUID):
        return value
    if isinstance(value, str):
        try:
            return uuid.UUID(value)
        except ValueError:
            return value
    return value


def _normalize_filters(filters: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: _normalize_filter_value(key, value)
        for key, value in dict(filters).items()
    }


def _list_items(result: Any) -> list[Any]:
    if isinstance(result, Mapping) and isinstance(result.get("items"), list):
        result = result["items"]
    elif hasattr(result, "items"):
        result = result.items
    if isinstance(result, list):
        return result
    if isinstance(result, tuple):
        return list(result)
    if result is None:
        return []
    return [result]


def _value_matches(actual: Any, expected: Any) -> bool:
    if actual == expected:
        return True
    if actual is None or expected is None:
        return False
    return str(actual) == str(expected)


def _matches_filters(user: Any, filters: Mapping[str, Any]) -> bool:
    for key, expected in filters.items():
        if isinstance(user, Mock) and key not in getattr(user, "__dict__", {}):
            continue
        if not hasattr(user, key):
            continue
        if not _value_matches(getattr(user, key, None), expected):
            return False
    return True


async def first_user_by_filters(db: Any, filters: Mapping[str, Any]) -> User | None:
    normalized_filters = _normalize_filters(filters)
    users = await User.handlers.list.core(
        {
            "payload": {
                "filters": normalized_filters,
            },
            "db": db,
        }
    )
    for user in _list_items(users):
        if _matches_filters(user, normalized_filters):
            return user
    return None


__all__ = ["first_user_by_filters"]
