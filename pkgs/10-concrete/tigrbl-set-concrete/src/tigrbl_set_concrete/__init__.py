"""RFC 8417 Security Event Token claim construction and validation."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from time import time
from typing import Any
from uuid import uuid4

from tigrbl_identity_core import require_absolute_uri

RFC8417_SPEC_URL = "https://www.rfc-editor.org/rfc/rfc8417"
SET_TYP = "secevent+jwt"


class SecurityEventTokenError(ValueError):
    """Raised when claims do not satisfy the RFC 8417 SET profile."""


def build_security_event_claims(
    *,
    issuer: str,
    audience: str | Sequence[str],
    events: Mapping[str, Mapping[str, Any] | None],
    subject: str | None = None,
    issued_at: int | None = None,
    token_id: str | None = None,
    expires_at: int | None = None,
) -> dict[str, Any]:
    """Build the claims set for a Security Event Token.

    Signing and JOSE header construction are intentionally delegated to a JOSE
    provider. The caller must use the ``secevent+jwt`` explicit type.
    """

    claims: dict[str, Any] = {
        "iss": require_absolute_uri(issuer, https=True),
        "aud": _normalize_audience(audience),
        "iat": int(time()) if issued_at is None else int(issued_at),
        "jti": str(token_id or uuid4()),
        "events": _normalize_events(events),
    }
    if subject is not None:
        normalized_subject = str(subject).strip()
        if not normalized_subject:
            raise SecurityEventTokenError("sub must not be empty")
        claims["sub"] = normalized_subject
    if expires_at is not None:
        claims["exp"] = int(expires_at)
    return claims


def validate_security_event_claims(
    claims: Mapping[str, Any],
    *,
    expected_issuer: str | None = None,
    expected_audience: str | None = None,
    now: int | None = None,
) -> dict[str, Any]:
    """Validate decoded JWT claims against the RFC 8417 SET profile."""

    required = ("iss", "aud", "iat", "jti", "events")
    missing = [name for name in required if name not in claims]
    if missing:
        raise SecurityEventTokenError(f"missing required SET claims: {', '.join(missing)}")
    normalized = dict(claims)
    normalized["iss"] = require_absolute_uri(str(claims["iss"]), https=True)
    normalized["aud"] = _normalize_audience(claims["aud"])
    normalized["events"] = _normalize_events(claims["events"])
    try:
        normalized["iat"] = int(claims["iat"])
    except (TypeError, ValueError) as exc:
        raise SecurityEventTokenError("iat must be an integer timestamp") from exc
    if not str(claims["jti"]).strip():
        raise SecurityEventTokenError("jti must not be empty")
    normalized["jti"] = str(claims["jti"])
    if "sub" in claims and not isinstance(claims["sub"], str):
        raise SecurityEventTokenError("sub must be a string when present")
    if expected_issuer is not None and normalized["iss"] != expected_issuer:
        raise SecurityEventTokenError("invalid SET issuer")
    if expected_audience is not None:
        audience_values = [normalized["aud"]] if isinstance(normalized["aud"], str) else normalized["aud"]
        if expected_audience not in audience_values:
            raise SecurityEventTokenError("invalid SET audience")
    current = int(time()) if now is None else int(now)
    if "exp" in claims:
        try:
            normalized["exp"] = int(claims["exp"])
        except (TypeError, ValueError) as exc:
            raise SecurityEventTokenError("exp must be an integer timestamp") from exc
        if normalized["exp"] <= current:
            raise SecurityEventTokenError("SET has expired")
    return normalized


def event_data(claims: Mapping[str, Any], event_type: str) -> Mapping[str, Any] | None:
    """Return event data from claims that were already profile-validated."""

    events = _normalize_events(claims.get("events"))
    return events.get(event_type)


def _normalize_audience(value: object) -> str | list[str]:
    if isinstance(value, str):
        normalized = value.strip()
        if not normalized:
            raise SecurityEventTokenError("aud must not be empty")
        return normalized
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        normalized = [str(item).strip() for item in value]
        if not normalized or any(not item for item in normalized):
            raise SecurityEventTokenError("aud must contain non-empty values")
        return normalized
    raise SecurityEventTokenError("aud must be a string or array of strings")


def _normalize_events(value: object) -> dict[str, dict[str, Any]]:
    if not isinstance(value, Mapping) or not value:
        raise SecurityEventTokenError("events must be a non-empty object")
    result: dict[str, dict[str, Any]] = {}
    for event_type, data in value.items():
        event_uri = require_absolute_uri(str(event_type), https=True)
        if data is None:
            result[event_uri] = {}
        elif isinstance(data, Mapping):
            result[event_uri] = dict(data)
        else:
            raise SecurityEventTokenError("event data must be an object")
    return result


__all__ = [
    "RFC8417_SPEC_URL", "SET_TYP", "SecurityEventTokenError",
    "build_security_event_claims", "event_data", "validate_security_event_claims",
]
