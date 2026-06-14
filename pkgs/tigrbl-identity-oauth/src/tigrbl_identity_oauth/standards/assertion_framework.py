from __future__ import annotations

"""RFC 7521 assertion-framework helpers.

This module owns the runtime validation and contract helpers for JWT bearer
assertion grants and client assertions at the token endpoint.
"""

import time
from dataclasses import dataclass
from typing import Any, Final, Iterable

from tigrbl_identity_runtime.settings import settings
from tigrbl_identity_core.errors import InvalidTokenError
from tigrbl_identity_jose.standards.rfc7519 import decode_jwt

STATUS: Final[str] = "assertion-framework-runtime-integrated"
RFC7521_SPEC_URL: Final[str] = "https://www.rfc-editor.org/rfc/rfc7521"
JWT_BEARER_GRANT_TYPE: Final[str] = "urn:ietf:params:oauth:grant-type:jwt-bearer"
JWT_BEARER_ASSERTION_TYPE: Final[str] = "urn:ietf:params:oauth:client-assertion-type:jwt-bearer"
REQUIRED_CLAIMS: Final[set[str]] = {"iss", "sub", "aud", "exp"}
OPTIONAL_FRESHNESS_CLAIMS: Final[set[str]] = {"iat", "nbf", "jti"}


@dataclass(frozen=True, slots=True)
class StandardOwner:
    label: str
    title: str
    runtime_status: str
    public_surface: tuple[str, ...]
    notes: str


OWNER = StandardOwner(
    label="RFC 7521",
    title="Assertion Framework for OAuth 2.0 Client Authentication and Authorization Grants",
    runtime_status=STATUS,
    public_surface=("/token",),
    notes=(
        "Runtime-integrated JWT bearer assertion validation for assertion grants and "
        "client_assertion payloads at the token endpoint."
    ),
)



def _coerce_audiences(audience: str | Iterable[str] | None) -> set[str]:
    if audience is None:
        return set()
    if isinstance(audience, str):
        return {audience}
    return {str(item) for item in audience}



def _coerce_aud_claim(value: object) -> set[str]:
    if isinstance(value, str):
        return {value}
    if isinstance(value, (list, tuple, set)):
        return {str(item) for item in value}
    raise ValueError("invalid aud claim")



def _require_timestamp(claims: dict[str, object], name: str) -> int:
    value = claims.get(name)
    if not isinstance(value, int):
        raise InvalidTokenError(f"'{name}' claim must be an integer timestamp")
    return value



def validate_temporal_claims(
    claims: dict[str, object],
    *,
    now: int | None = None,
    leeway_seconds: int = 30,
) -> None:
    current = int(time.time()) if now is None else int(now)
    exp = _require_timestamp(claims, "exp")
    if exp <= current - leeway_seconds:
        raise InvalidTokenError("assertion is expired")
    nbf = claims.get("nbf")
    if nbf is not None:
        if not isinstance(nbf, int):
            raise InvalidTokenError("'nbf' claim must be an integer timestamp")
        if nbf > current + leeway_seconds:
            raise InvalidTokenError("assertion is not yet valid")
    iat = claims.get("iat")
    if iat is not None:
        if not isinstance(iat, int):
            raise InvalidTokenError("'iat' claim must be an integer timestamp")
        if iat > current + leeway_seconds:
            raise InvalidTokenError("assertion 'iat' claim is in the future")



def validate_jwt_assertion(
    assertion: str,
    *,
    audience: str | Iterable[str] | None = None,
    expected_issuer: str | None = None,
    expected_subject: str | None = None,
    now: int | None = None,
    leeway_seconds: int = 30,
    decoder=decode_jwt,
) -> dict[str, object]:
    """Validate a JWT bearer assertion per RFC 7521."""

    if not settings.enable_rfc7521:
        raise RuntimeError(f"RFC 7521 support disabled: {RFC7521_SPEC_URL}")
    claims = dict(decoder(assertion))
    missing = REQUIRED_CLAIMS - claims.keys()
    if missing:
        raise ValueError(f"missing claims: {', '.join(sorted(missing))}")
    validate_temporal_claims(claims, now=now, leeway_seconds=leeway_seconds)
    if expected_issuer is not None and claims.get("iss") != expected_issuer:
        raise ValueError("invalid issuer")
    if expected_subject is not None and claims.get("sub") != expected_subject:
        raise ValueError("invalid subject")
    expected_audiences = _coerce_audiences(audience)
    if expected_audiences:
        aud_values = _coerce_aud_claim(claims["aud"])
        if aud_values.isdisjoint(expected_audiences):
            raise ValueError("invalid audience")
    return claims



def validate_assertion_grant_request(
    request_data: dict[str, str],
    *,
    audience: str | Iterable[str] | None,
    now: int | None = None,
) -> dict[str, object]:
    if str(request_data.get("grant_type") or "") != JWT_BEARER_GRANT_TYPE:
        raise ValueError("invalid grant_type for RFC 7521 assertion processing")
    assertion = str(request_data.get("assertion") or "").strip()
    if not assertion:
        raise ValueError("assertion parameter is required")
    return validate_jwt_assertion(assertion, audience=audience, now=now)



def build_assertion_contract_examples(token_endpoint_audience: str) -> list[dict[str, Any]]:
    return [
        {
            "grant_type": JWT_BEARER_GRANT_TYPE,
            "assertion": "<jwt-bearer-assertion>",
            "scope": "openid profile email",
            "client_id": "<client-id>",
            "client_assertion_type": JWT_BEARER_ASSERTION_TYPE,
            "client_assertion": "<client-auth-assertion>",
            "audience": token_endpoint_audience,
        }
    ]



def describe() -> dict[str, object]:
    return {
        "label": OWNER.label,
        "title": OWNER.title,
        "runtime_status": OWNER.runtime_status,
        "public_surface": list(OWNER.public_surface),
        "notes": OWNER.notes,
        "spec_url": RFC7521_SPEC_URL,
        "assertion_grant_type": JWT_BEARER_GRANT_TYPE,
        "client_assertion_type": JWT_BEARER_ASSERTION_TYPE,
    }


__all__ = [
    "STATUS",
    "RFC7521_SPEC_URL",
    "JWT_BEARER_GRANT_TYPE",
    "JWT_BEARER_ASSERTION_TYPE",
    "REQUIRED_CLAIMS",
    "OPTIONAL_FRESHNESS_CLAIMS",
    "StandardOwner",
    "OWNER",
    "build_assertion_contract_examples",
    "describe",
    "validate_assertion_grant_request",
    "validate_jwt_assertion",
    "validate_temporal_claims",
]
