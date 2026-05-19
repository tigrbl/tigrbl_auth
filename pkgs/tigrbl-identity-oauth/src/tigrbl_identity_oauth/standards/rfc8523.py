"""Legacy migration-history compatibility module for the historical RFC 8523 label.

Certification claims map JWT client authentication to RFC 7523. This module
preserves the legacy helper API without relying on the flat ``tigrbl_auth.rfc``
tree.
"""

from __future__ import annotations

import time
import warnings
from typing import Any, Iterable

from tigrbl_auth.config.settings import settings
from tigrbl_auth.errors import InvalidTokenError
from tigrbl_auth.standards.jose.rfc7519 import encode_jwt
from tigrbl_auth.standards.oauth2.jwt_client_auth import validate_client_jwt_bearer

RFC8523_SPEC_URL = "https://www.rfc-editor.org/rfc/rfc8523"
REQUIRED_CLAIMS: set[str] = {"iss", "sub", "aud", "exp", "iat", "jti"}


def validate_enhanced_jwt_bearer(
    assertion: str,
    *,
    audience: str | Iterable[str] | None = None,
    max_age_seconds: int = 300,
    clock_skew_seconds: int = 30,
) -> dict[str, Any]:
    if not settings.enable_rfc8523:
        raise RuntimeError("Legacy RFC 8523 path disabled")
    claims = validate_client_jwt_bearer(assertion, audience=audience)
    missing = REQUIRED_CLAIMS - claims.keys()
    if missing:
        raise ValueError(f"Legacy RFC 8523 path missing claims: {', '.join(sorted(missing))}")
    current_time = int(time.time())
    iat = claims.get("iat")
    if not isinstance(iat, int):
        raise InvalidTokenError("'iat' claim must be an integer timestamp")
    token_age = current_time - iat
    if token_age > max_age_seconds + clock_skew_seconds:
        raise ValueError(f"JWT is too old: {token_age} seconds > {max_age_seconds}")
    if iat > current_time + clock_skew_seconds:
        raise InvalidTokenError("JWT 'iat' claim is in the future")
    jti = claims.get("jti")
    if not isinstance(jti, str) or not jti.strip():
        raise ValueError("'jti' claim must be a non-empty string")
    return claims


def makeClientAssertionJwt(
    client_id: str,
    audience: str,
    *,
    expires_in: int = 300,
    additional_claims: dict[str, Any] | None = None,
) -> str:
    if not settings.enable_rfc8523:
        raise RuntimeError("Legacy RFC 8523 path disabled")
    import uuid

    current_time = int(time.time())
    claims = {
        "iss": client_id,
        "sub": client_id,
        "aud": audience,
        "exp": current_time + expires_in,
        "iat": current_time,
        "jti": str(uuid.uuid4()),
    }
    if additional_claims:
        claims.update(additional_claims)
    return encode_jwt(**claims)


def create_client_assertion_jwt(
    client_id: str,
    audience: str,
    *,
    expires_in: int = 300,
    additional_claims: dict[str, Any] | None = None,
) -> str:
    warnings.warn(
        "create_client_assertion_jwt is deprecated, use makeClientAssertionJwt",
        DeprecationWarning,
        stacklevel=2,
    )
    return makeClientAssertionJwt(
        client_id,
        audience,
        expires_in=expires_in,
        additional_claims=additional_claims,
    )


def is_jwt_replay(jti: str, iat: int, max_age_seconds: int = 300) -> bool:
    return False


__all__ = [
    "validate_enhanced_jwt_bearer",
    "makeClientAssertionJwt",
    "create_client_assertion_jwt",
    "is_jwt_replay",
    "RFC8523_SPEC_URL",
    "REQUIRED_CLAIMS",
]
