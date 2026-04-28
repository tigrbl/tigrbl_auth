from __future__ import annotations

"""RFC 7523 JWT client-auth helpers."""

import time
import uuid
from dataclasses import dataclass
from typing import Any, Final, Iterable

from tigrbl_auth.config.settings import settings
from tigrbl_auth.standards.oauth2.mtls import SUPPORTED_MTLS_AUTH_METHODS
from tigrbl_auth.standards.jose.rfc7519 import decode_jwt, encode_jwt
from tigrbl_auth.standards.oauth2.assertion_framework import (
    JWT_BEARER_ASSERTION_TYPE,
    validate_temporal_claims,
)

STATUS: Final[str] = "jwt-client-auth-runtime-integrated"
RFC7523_SPEC_URL: Final[str] = "https://www.rfc-editor.org/rfc/rfc7523"
REQUIRED_CLAIMS: Final[set[str]] = {"iss", "sub", "aud", "exp"}
STRICT_CLIENT_ASSERTION_CLAIMS: Final[set[str]] = REQUIRED_CLAIMS | {"iat", "jti"}
PRIVATE_KEY_JWT_AUTH_METHOD: Final[str] = "private_key_jwt"
CLIENT_SECRET_JWT_AUTH_METHOD: Final[str] = "client_secret_jwt"
SUPPORTED_CLIENT_ASSERTION_AUTH_METHODS: Final[tuple[str, ...]] = (PRIVATE_KEY_JWT_AUTH_METHOD,)
SUPPORTED_CLIENT_ASSERTION_SIGNING_ALGS: Final[tuple[str, ...]] = ("EdDSA",)


@dataclass(frozen=True, slots=True)
class StandardOwner:
    label: str
    title: str
    runtime_status: str
    public_surface: tuple[str, ...]
    notes: str


OWNER = StandardOwner(
    label="RFC 7523",
    title="JWT Profile for OAuth 2.0 Client Authentication and Authorization Grants",
    runtime_status=STATUS,
    public_surface=("/token",),
    notes="Runtime-integrated JWT bearer assertion validation for token-endpoint client authentication and authorization grants.",
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



def validate_client_jwt_bearer(
    assertion: str,
    *,
    audience: str | Iterable[str] | None = None,
    client_id: str | None = None,
    now: int | None = None,
    leeway_seconds: int = 30,
    require_strict_claims: bool = False,
    decoder=decode_jwt,
) -> dict[str, object]:
    """Validate a client assertion per RFC 7523."""

    if not settings.enable_rfc7523:
        raise RuntimeError(f"RFC 7523 support disabled: {RFC7523_SPEC_URL}")
    claims = dict(decoder(assertion))
    required_claims = STRICT_CLIENT_ASSERTION_CLAIMS if require_strict_claims else REQUIRED_CLAIMS
    missing = required_claims - claims.keys()
    if missing:
        raise ValueError(f"missing claims: {', '.join(sorted(missing))}")
    validate_temporal_claims(claims, now=now, leeway_seconds=leeway_seconds)
    iss = str(claims.get("iss") or "")
    sub = str(claims.get("sub") or "")
    if iss != sub:
        raise ValueError("iss and sub must match for client authentication")
    if client_id is not None and iss != client_id:
        raise ValueError("client assertion subject does not match client_id")
    expected_audiences = _coerce_audiences(audience)
    if expected_audiences:
        aud_values = _coerce_aud_claim(claims["aud"])
        if aud_values.isdisjoint(expected_audiences):
            raise ValueError("invalid audience")
    if require_strict_claims:
        jti = claims.get("jti")
        if not isinstance(jti, str) or not jti.strip():
            raise ValueError("missing claims: jti")
    return claims



def authenticate_client_assertion(
    *,
    client_assertion_type: str,
    client_assertion: str,
    audience: str | Iterable[str] | None,
    client_id: str | None = None,
    token_endpoint_auth_method: str | None = None,
) -> dict[str, object]:
    if not settings.enable_rfc7523:
        raise RuntimeError(f"RFC 7523 support disabled: {RFC7523_SPEC_URL}")
    if client_assertion_type != JWT_BEARER_ASSERTION_TYPE:
        raise ValueError("unsupported client_assertion_type")
    if token_endpoint_auth_method not in {None, PRIVATE_KEY_JWT_AUTH_METHOD, CLIENT_SECRET_JWT_AUTH_METHOD}:
        raise ValueError("unsupported token_endpoint_auth_method")
    return validate_client_jwt_bearer(
        client_assertion,
        audience=audience,
        client_id=client_id,
        require_strict_claims=True,
    )



def make_client_assertion_jwt(
    client_id: str,
    audience: str,
    *,
    expires_in: int = 300,
    additional_claims: dict[str, Any] | None = None,
) -> str:
    """Mint a client assertion JWT suitable for RFC 7523 flows."""

    if not settings.enable_rfc7523:
        raise RuntimeError(f"RFC 7523 support disabled: {RFC7523_SPEC_URL}")
    current_time = int(time.time())
    claims: dict[str, Any] = {
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



def token_endpoint_auth_methods_supported() -> list[str]:
    methods = ["client_secret_basic", "client_secret_post"]
    if settings.enable_rfc7523:
        methods.append(PRIVATE_KEY_JWT_AUTH_METHOD)
    if settings.enable_rfc8705:
        methods.extend(SUPPORTED_MTLS_AUTH_METHODS)
    return list(dict.fromkeys(methods))



def token_endpoint_auth_signing_alg_values_supported() -> list[str]:
    return list(SUPPORTED_CLIENT_ASSERTION_SIGNING_ALGS) if settings.enable_rfc7523 else []



def build_client_assertion_contract_examples(token_endpoint_audience: str) -> list[dict[str, Any]]:
    return [
        {
            "client_id": "<client-id>",
            "client_assertion_type": JWT_BEARER_ASSERTION_TYPE,
            "client_assertion": "<jwt-client-assertion>",
            "token_endpoint_auth_method": PRIVATE_KEY_JWT_AUTH_METHOD,
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
        "spec_url": RFC7523_SPEC_URL,
        "token_endpoint_auth_methods_supported": token_endpoint_auth_methods_supported(),
        "token_endpoint_auth_signing_alg_values_supported": token_endpoint_auth_signing_alg_values_supported(),
    }


__all__ = [
    "STATUS",
    "RFC7523_SPEC_URL",
    "REQUIRED_CLAIMS",
    "STRICT_CLIENT_ASSERTION_CLAIMS",
    "PRIVATE_KEY_JWT_AUTH_METHOD",
    "CLIENT_SECRET_JWT_AUTH_METHOD",
    "SUPPORTED_CLIENT_ASSERTION_AUTH_METHODS",
    "SUPPORTED_CLIENT_ASSERTION_SIGNING_ALGS",
    "StandardOwner",
    "OWNER",
    "JWT_BEARER_ASSERTION_TYPE",
    "authenticate_client_assertion",
    "build_client_assertion_contract_examples",
    "describe",
    "make_client_assertion_jwt",
    "token_endpoint_auth_methods_supported",
    "token_endpoint_auth_signing_alg_values_supported",
    "validate_client_jwt_bearer",
]
