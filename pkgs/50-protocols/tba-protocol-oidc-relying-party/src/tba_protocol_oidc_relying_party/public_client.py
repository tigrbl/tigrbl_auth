"""Wire validation for the public Authorization Code with S256 profile."""

from __future__ import annotations

import json
import math
from typing import Any, Mapping
from urllib.parse import parse_qs, urlsplit

from tba_concrete_jws import parse_jws_compact
from tba_provider_jose_cryptography.public_jws import verify_public_jws

from .errors import RPError


def https_url(value: object, name: str) -> str:
    if (
        not isinstance(value, str)
        or not value
        or any(char.isspace() or ord(char) < 32 or char == "\\" for char in value)
    ):
        raise RPError(f"invalid {name} URL")
    try:
        parts = urlsplit(value)
        parts.port
    except ValueError as exc:
        raise RPError(f"invalid {name} URL") from exc
    if (
        parts.scheme != "https"
        or not parts.hostname
        or parts.username is not None
        or "#" in value
    ):
        raise RPError(f"invalid {name} URL")
    return value


def check_callback(url: str, redirect_uri: str) -> None:
    actual = urlsplit(https_url(url, "callback"))
    expected = urlsplit(https_url(redirect_uri, "redirect URI"))
    if (actual.scheme, actual.netloc, actual.path) != (
        expected.scheme,
        expected.netloc,
        expected.path,
    ):
        raise RPError("callback URL does not match the registered redirect URI")
    query = parse_qs(actual.query, keep_blank_values=True)
    fixed = parse_qs(expected.query, keep_blank_values=True)
    reserved = {"code", "state", "iss", "error", "error_description", "error_uri"}
    if reserved.intersection(fixed) or any(
        query.get(key) != value for key, value in fixed.items()
    ):
        raise RPError("callback URL does not match the registered redirect URI")
    if any(len(query.get(key, ())) > 1 for key in reserved):
        raise RPError("callback contains duplicate protocol parameters")
    if "iss" in query and not query["iss"][0]:
        raise RPError("callback issuer mismatch")


def check_discovery(metadata: Mapping[str, Any], issuer: str) -> None:
    if not isinstance(metadata, Mapping) or metadata.get("issuer") != issuer:
        raise RPError("issuer metadata mismatch")
    for key in ("authorization_endpoint", "token_endpoint", "jwks_uri"):
        https_url(metadata.get(key), key)
    for key, supported in (
        ("code_challenge_methods_supported", "S256"),
        ("token_endpoint_auth_methods_supported", "none"),
        ("id_token_signing_alg_values_supported", "RS256"),
    ):
        values = metadata.get(key)
        if values is not None and (
            not isinstance(values, list) or supported not in values
        ):
            raise RPError(f"issuer does not support {supported} in {key}")


def token_claims(token: str, jwks: Mapping[str, Any]) -> Mapping[str, Any]:
    try:
        jws = parse_jws_compact(token)
        header = jws.protected_headers
        kid = header.get("kid")
        if header.get("alg") != "RS256" or not isinstance(kid, str) or not kid:
            raise ValueError("unexpected algorithm or key ID")
        keys = jwks.get("keys") if isinstance(jwks, Mapping) else None
        if not isinstance(keys, list):
            raise ValueError("invalid JWKS")
        matching = [
            key for key in keys if isinstance(key, Mapping) and key.get("kid") == kid
        ]
        (key,) = matching
        if key.get("use", "sig") != "sig":
            raise ValueError("key is outside the signature-use profile")
        verify_public_jws(token, key)
        claims = json.loads(jws.payload.decode("utf-8"))
        if not isinstance(claims, dict):
            raise ValueError("expected a claims object")
        for name in ("exp", "iat", "nbf"):
            if name == "nbf" and name not in claims:
                continue
            value = claims.get(name)
            if type(value) not in (int, float) or not math.isfinite(value):
                raise ValueError(f"invalid {name}")
        audiences = claims.get("aud")
        if isinstance(audiences, str):
            audiences = [audiences]
        if (
            not isinstance(audiences, list)
            or not audiences
            or not all(isinstance(item, str) and item for item in audiences)
        ):
            raise ValueError("invalid audience")
        if not isinstance(claims.get("sub"), str) or not claims["sub"]:
            raise ValueError("invalid subject")
    except (ValueError, TypeError, KeyError, OverflowError) as exc:
        raise RPError("ID token signature or structure is invalid") from exc
    return claims
