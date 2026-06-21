"""Sensitive field redaction helpers shared by identity packages."""

from __future__ import annotations

from typing import Any, Mapping

SECRET_FIELD_TOKENS: tuple[str, ...] = (
    "secret",
    "password",
    "token",
    "assertion",
    "private_key",
    "client_secret",
)


def redact_sensitive_mapping(values: Mapping[str, Any]) -> dict[str, Any]:
    """Return a copy of a mapping with sensitive nested fields redacted."""

    redacted: dict[str, Any] = {}
    for key, value in values.items():
        key_text = str(key)
        if any(token in key_text.lower() for token in SECRET_FIELD_TOKENS):
            redacted[key_text] = "[REDACTED]"
        elif isinstance(value, Mapping):
            redacted[key_text] = redact_sensitive_mapping(value)
        else:
            redacted[key_text] = value
    return redacted


__all__ = ["SECRET_FIELD_TOKENS", "redact_sensitive_mapping"]
