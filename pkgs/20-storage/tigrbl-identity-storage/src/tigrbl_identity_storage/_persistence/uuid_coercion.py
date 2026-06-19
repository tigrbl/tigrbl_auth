from __future__ import annotations

from typing import Any, Mapping
from uuid import UUID

UUID_FILTER_KEYS = {
    "id",
    "tenant_id",
    "user_id",
    "client_id",
    "session_id",
    "logout_id",
    "consent_id",
    "actor_user_id",
    "actor_client_id",
}


def coerce_uuid_value(value: Any) -> Any:
    if value in {None, "", False}:
        return value
    if isinstance(value, UUID):
        return value
    try:
        return UUID(str(value))
    except Exception:
        return value


def normalize_uuid_identifier(value: Any) -> Any:
    return coerce_uuid_value(value)


def normalize_uuid_filters(filters: Mapping[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for key, value in filters.items():
        normalized[key] = coerce_uuid_value(value) if key in UUID_FILTER_KEYS else value
    return normalized
