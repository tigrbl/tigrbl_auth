"""Compatibility facade for OIDC ID token helpers.

The package-level module keeps historical imports stable while allowing test
fixtures to mutate the exported key-provider state in one place. When the full
runtime stack is available, mutable facade globals are synchronized into the
canonical implementation before each helper call.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from functools import lru_cache
from hashlib import sha256
from typing import Any, Iterable, Mapping
import base64
import os
import pathlib
import secrets

from tigrbl_auth.config.settings import settings
from tigrbl_auth.errors import InvalidTokenError
from tigrbl_auth.standards.jose.rfc7516 import decrypt_jwe, encrypt_jwe
from tigrbl_auth.standards.jose.rfc7519 import decode_jwt, encode_jwt

_CANONICAL = None
try:  # pragma: no cover - exercised when runtime dependencies are installed
    import tigrbl_auth.standards.oidc.id_token as _CANONICAL  # type: ignore[assignment]
except Exception:  # pragma: no cover - dependency-light fallback
    _CANONICAL = None


if _CANONICAL is not None:  # pragma: no cover - covered indirectly in tests
    _RSA_KEY_PATH = _CANONICAL._RSA_KEY_PATH
    _provider = _CANONICAL._provider
    _service_cache = _CANONICAL._service_cache

    def _sync_to_canonical() -> None:
        next_path = globals().get("_RSA_KEY_PATH", _CANONICAL._RSA_KEY_PATH)
        if next_path != _CANONICAL._RSA_KEY_PATH:
            _CANONICAL._RSA_KEY_PATH = next_path
            _CANONICAL._service_cache = None
            try:
                _CANONICAL._provider.cache_clear()
            except Exception:
                pass
        else:
            _CANONICAL._RSA_KEY_PATH = next_path

    def _sync_from_canonical() -> None:
        globals()["_RSA_KEY_PATH"] = _CANONICAL._RSA_KEY_PATH
        globals()["_service_cache"] = _CANONICAL._service_cache

    def oidc_hash(value: str) -> str:
        return _CANONICAL.oidc_hash(value)

    async def mint_id_token(
        *,
        sub: str,
        aud: Iterable[str] | str,
        nonce: str,
        issuer: str,
        ttl: timedelta = timedelta(minutes=5),
        **extra: Mapping[str, Any] | Any,
    ) -> str:
        _sync_to_canonical()
        try:
            return await _CANONICAL.mint_id_token(
                sub=sub, aud=aud, nonce=nonce, issuer=issuer, ttl=ttl, **extra
            )
        finally:
            _sync_from_canonical()

    async def verify_id_token(
        token: str, *, issuer: str, audience: Iterable[str] | str
    ) -> dict[str, Any]:
        _sync_to_canonical()
        try:
            return await _CANONICAL.verify_id_token(token, issuer=issuer, audience=audience)
        finally:
            _sync_from_canonical()

    def rsa_key_provider():
        _sync_to_canonical()
        provider = _CANONICAL.rsa_key_provider()
        _sync_from_canonical()
        return provider

    async def ensure_rsa_jwt_key() -> tuple[str, bytes, bytes]:
        _sync_to_canonical()
        try:
            return await _CANONICAL.ensure_rsa_jwt_key()
        finally:
            _sync_from_canonical()

    async def rotate_rsa_jwt_key() -> str:
        _sync_to_canonical()
        try:
            return await _CANONICAL.rotate_rsa_jwt_key()
        finally:
            _sync_from_canonical()

else:  # pragma: no cover - dependency-light fallback
    _RSA_KEY_PATH = pathlib.Path(os.getenv("JWT_RS256_KEY_PATH", "runtime_secrets/jwt_rs256.kid"))
    _service_cache = None

    @lru_cache(maxsize=1)
    def _provider():
        return None

    def oidc_hash(value: str) -> str:
        digest = sha256(value.encode("ascii")).digest()
        half = digest[: len(digest) // 2]
        return base64.urlsafe_b64encode(half).decode("ascii").rstrip("=")

    async def mint_id_token(
        *,
        sub: str,
        aud: Iterable[str] | str,
        nonce: str,
        issuer: str,
        ttl: timedelta = timedelta(minutes=5),
        **extra: Mapping[str, Any] | Any,
    ) -> str:
        now = datetime.now(timezone.utc)
        claims: dict[str, Any] = {
            "iss": issuer,
            "sub": sub,
            "aud": aud,
            "iat": int(now.timestamp()),
            "exp": int((now + ttl).timestamp()),
            "nonce": nonce,
        }
        if extra:
            claims.update(extra)  # type: ignore[arg-type]
        token = encode_jwt(**claims)
        if settings.enable_id_token_encryption:
            token = await encrypt_jwe(token, {"kty": "oct", "k": settings.id_token_encryption_key.encode()})
        return token

    async def verify_id_token(token: str, *, issuer: str, audience: Iterable[str] | str) -> dict[str, Any]:
        if settings.enable_id_token_encryption:
            token = await decrypt_jwe(token, {"kty": "oct", "k": settings.id_token_encryption_key.encode()})
        claims = decode_jwt(token)
        if claims.get("iss") != issuer:
            raise InvalidTokenError("invalid issuer")
        expected_audiences = {audience} if isinstance(audience, str) else {str(item) for item in audience}
        aud_claim = claims.get("aud")
        if isinstance(aud_claim, str):
            actual_audiences = {aud_claim}
        elif isinstance(aud_claim, (list, tuple, set)):
            actual_audiences = {str(item) for item in aud_claim}
        else:
            raise InvalidTokenError("invalid audience claim")
        if actual_audiences.isdisjoint(expected_audiences):
            raise InvalidTokenError("invalid audience")
        return claims

    def rsa_key_provider():
        return None

    async def ensure_rsa_jwt_key() -> tuple[str, bytes, bytes]:
        kid = _RSA_KEY_PATH.read_text().strip() if _RSA_KEY_PATH.exists() else "checkpoint-hs256"
        material = settings.jwt_secret.encode("utf-8")
        return kid, material, material

    async def rotate_rsa_jwt_key() -> str:
        kid = f"checkpoint-{secrets.token_hex(8)}"
        _RSA_KEY_PATH.parent.mkdir(parents=True, exist_ok=True)
        _RSA_KEY_PATH.write_text(kid)
        try:
            from tigrbl_auth.oidc_discovery import refresh_discovery_cache

            refresh_discovery_cache()
        except Exception:
            pass
        return kid


__all__ = [
    "mint_id_token",
    "verify_id_token",
    "oidc_hash",
    "rsa_key_provider",
    "ensure_rsa_jwt_key",
    "rotate_rsa_jwt_key",
]
