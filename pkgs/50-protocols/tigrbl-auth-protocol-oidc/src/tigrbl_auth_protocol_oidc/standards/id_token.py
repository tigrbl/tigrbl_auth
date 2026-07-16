"""OIDC ID Token wire claims, signing invocation, and validation rules."""

from __future__ import annotations

import base64
import json
from datetime import timedelta
from hashlib import sha256
from typing import Any, Iterable, Mapping

from swarmauri_core.crypto.types import JWAAlg
from tigrbl_identity_contracts.protocol_configuration import (
    protocol_settings as settings,
)
from tigrbl_identity_core.errors import InvalidTokenError
from tigrbl_jose_swarmauri_provider.oidc_key_runtime import (
    _RSA_KEY_PATH,  # noqa: F401 - private compatibility patch point
    ensure_rsa_jwt_key,
    id_token_service,
    rsa_key_provider,
    rotate_rsa_jwt_key as _rotate_rsa_jwt_key,
    rotation_jwks_cache,
)
from tigrbl_identity_jose.standards.rfc7516 import decrypt_jwe, encrypt_jwe

# Mutable compatibility hooks retained for one release boundary. Environment
# key operations remain implemented by the layer-20 provider.
_provider = rsa_key_provider
_service_cache = None


def _header_alg(token: str) -> str:
    try:
        segment = token.split(".")[0]
        header = json.loads(
            base64.urlsafe_b64decode(segment + "=" * (-len(segment) % 4))
        )
        return str(header.get("alg", "")).lower()
    except Exception:
        return ""


def oidc_hash(value: str) -> str:
    """Return the OIDC half-hash used by at_hash/c_hash/s_hash."""
    digest = sha256(value.encode("ascii")).digest()
    return (
        base64.urlsafe_b64encode(digest[: len(digest) // 2]).decode("ascii").rstrip("=")
    )


async def mint_id_token(
    *,
    sub: str,
    aud: Iterable[str] | str,
    nonce: str,
    issuer: str,
    ttl: timedelta = timedelta(minutes=5),
    **extra: Mapping[str, Any] | Any,
) -> str:
    service, kid = await id_token_service()
    claims: dict[str, Any] = {"nonce": nonce}
    claims.update(extra)
    token = await service.mint(
        claims,
        alg=JWAAlg.RS256,
        kid=kid,
        lifetime_s=int(ttl.total_seconds()),
        issuer=issuer,
        subject=sub,
        audience=aud,
    )
    if settings.enable_id_token_encryption:
        token = await encrypt_jwe(
            token, {"kty": "oct", "k": settings.id_token_encryption_key.encode()}
        )
    return token


async def verify_id_token(
    token: str, *, issuer: str, audience: Iterable[str] | str
) -> dict:
    if settings.enable_id_token_encryption:
        token = await decrypt_jwe(
            token, {"kty": "oct", "k": settings.id_token_encryption_key.encode()}
        )
    if _header_alg(token) in {"", "none"}:
        raise InvalidTokenError("unsigned JWTs are not accepted")
    service, _ = await id_token_service()
    return await service.verify(token, issuer=issuer, audience=audience)


async def rotate_rsa_jwt_key() -> str:
    return await _rotate_rsa_jwt_key()


__all__ = [
    "ensure_rsa_jwt_key",
    "mint_id_token",
    "oidc_hash",
    "rsa_key_provider",
    "rotate_rsa_jwt_key",
    "rotation_jwks_cache",
    "verify_id_token",
]
