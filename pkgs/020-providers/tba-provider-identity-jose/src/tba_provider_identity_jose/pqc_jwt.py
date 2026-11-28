"""Compact JWT helpers for ML-DSA-backed JOSE profiles."""

from __future__ import annotations

import json
from collections.abc import Iterable, Mapping
from typing import Any

from .key_management import load_pqc_public_jwk, load_pqc_signing_jwk
from .pqc import ML_DSA_65_ALG, PQC_SIGNATURE_ALGS, is_pqc_algorithm, normalize_pqc_algorithm
from .standards.rfc7515 import sign_jws, verify_jws


def configured_jwt_signing_alg(settings_obj: Any) -> str:
    alg = str(getattr(settings_obj, "jwt_signing_alg", "EdDSA") or "EdDSA")
    if is_pqc_algorithm(alg):
        return normalize_pqc_algorithm(alg)
    return alg


def pqc_jose_enabled(settings_obj: Any) -> bool:
    return bool(getattr(settings_obj, "enable_pqc_jose", False)) or configured_jwt_signing_alg(settings_obj) in PQC_SIGNATURE_ALGS


def require_pqc_jose_enabled(settings_obj: Any) -> None:
    if not pqc_jose_enabled(settings_obj):
        raise RuntimeError("ML-DSA-65 JOSE support is disabled")


def validate_pqc_jwt_claims(
    payload: Mapping[str, Any],
    *,
    issuer: str | None = None,
    audience: Iterable[str] | str | None = None,
) -> None:
    if issuer is not None and payload.get("iss") != issuer:
        raise ValueError("issuer mismatch")
    if audience is None:
        return
    expected = {audience} if isinstance(audience, str) else set(audience)
    actual = payload.get("aud")
    actual_values = {actual} if isinstance(actual, str) else set(actual or [])
    if not actual_values.intersection(expected):
        raise ValueError("audience mismatch")


async def sign_pqc_jwt(
    payload: Mapping[str, Any],
    *,
    key: Mapping[str, Any] | None = None,
) -> str:
    signing_key = key or load_pqc_signing_jwk()
    body = json.dumps(dict(payload), separators=(",", ":"), sort_keys=True)
    return await sign_jws(body, signing_key, alg=ML_DSA_65_ALG)


async def verify_pqc_jwt(
    token: str,
    *,
    key: Mapping[str, Any] | None = None,
    issuer: str | None = None,
    audience: Iterable[str] | str | None = None,
) -> dict[str, Any]:
    public_key = key or load_pqc_public_jwk()
    body = await verify_jws(token, public_key)
    payload = json.loads(body)
    if not isinstance(payload, dict):
        raise ValueError("JWT payload must be an object")
    validate_pqc_jwt_claims(payload, issuer=issuer, audience=audience)
    return payload


__all__ = [
    "ML_DSA_65_ALG",
    "configured_jwt_signing_alg",
    "pqc_jose_enabled",
    "require_pqc_jose_enabled",
    "sign_pqc_jwt",
    "validate_pqc_jwt_claims",
    "verify_pqc_jwt",
]
