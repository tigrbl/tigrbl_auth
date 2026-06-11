from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping


SECRET_FIELD_TOKENS: tuple[str, ...] = (
    "secret",
    "password",
    "token",
    "assertion",
    "private_key",
    "client_secret",
)


def _utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


def _utc_now_iso() -> str:
    return _utc_now().isoformat()


def _tenant_key(tenant_id: str, entity_id: str) -> str:
    return f"{tenant_id}:{entity_id}"


def _normalize_entity(entity_type: str, entity_id: str) -> str:
    return f"{entity_type}:{entity_id}"


def _redact_sensitive_mapping(values: Mapping[str, Any]) -> dict[str, Any]:
    redacted: dict[str, Any] = {}
    for key, value in values.items():
        key_text = str(key)
        if any(token in key_text.lower() for token in SECRET_FIELD_TOKENS):
            redacted[key_text] = "[REDACTED]"
        elif isinstance(value, Mapping):
            redacted[key_text] = _redact_sensitive_mapping(value)
        else:
            redacted[key_text] = value
    return redacted
