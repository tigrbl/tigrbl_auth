"""Environment-backed RSA key lifecycle for OIDC ID Tokens."""

from __future__ import annotations

import os
import pathlib
import secrets
import sys
from functools import lru_cache
from typing import Any

from swarmauri_core.crypto.types import ExportPolicy, KeyUse
from swarmauri_core.key_providers.types import KeyAlg, KeyClass, KeySpec
from swarmauri_keyprovider_file import FileKeyProvider
from swarmauri_tokens_jwt import JWTTokenService


_RSA_KEY_PATH = pathlib.Path(
    os.getenv("JWT_RS256_KEY_PATH", "runtime_secrets/jwt_rs256.kid")
)
_service_cache: tuple[JWTTokenService, str] | None = None
_rotation_jwks_cache: list[dict[str, Any]] = []


def _sync_key_path_from_root_facade() -> None:
    global _RSA_KEY_PATH, _service_cache
    facade = sys.modules.get("tigrbl_auth.oidc_id_token")
    root_path = getattr(facade, "_RSA_KEY_PATH", None)
    if root_path is None or pathlib.Path(root_path) == _RSA_KEY_PATH:
        return
    _RSA_KEY_PATH = pathlib.Path(root_path)
    _service_cache = None
    rsa_key_provider.cache_clear()


@lru_cache(maxsize=1)
def rsa_key_provider() -> FileKeyProvider:
    return FileKeyProvider(_RSA_KEY_PATH.parent)


async def _create_rsa_key():
    ref = await rsa_key_provider().create_key(
        KeySpec(
            klass=KeyClass.asymmetric,
            alg=KeyAlg.RSA_PSS_SHA256,
            uses=(KeyUse.SIGN, KeyUse.VERIFY),
            export_policy=ExportPolicy.SECRET_WHEN_ALLOWED,
            label="jwt_rs256",
        )
    )
    _RSA_KEY_PATH.parent.mkdir(parents=True, exist_ok=True)
    _RSA_KEY_PATH.write_text(ref.kid)
    return ref


async def ensure_rsa_jwt_key() -> tuple[str, bytes, bytes]:
    _sync_key_path_from_root_facade()
    provider = rsa_key_provider()
    ref = None
    if _RSA_KEY_PATH.exists():
        kid = _RSA_KEY_PATH.read_text().strip()
        if kid:
            try:
                ref = await provider.get_key(kid, include_secret=True)
            except Exception:
                pass
    if ref is None:
        ref = await _create_rsa_key()
    return ref.kid, ref.material or b"", ref.public or b""


async def id_token_service() -> tuple[JWTTokenService, str]:
    global _service_cache
    if _service_cache is None:
        kid, _, _ = await ensure_rsa_jwt_key()
        _service_cache = (JWTTokenService(rsa_key_provider()), kid)
    else:
        service, kid = _service_cache
        try:
            await rsa_key_provider().get_key(kid, include_secret=False)
        except Exception:
            kid, _, _ = await ensure_rsa_jwt_key()
            _service_cache = (JWTTokenService(rsa_key_provider()), kid)
    return _service_cache


async def rotate_rsa_jwt_key() -> str:
    global _service_cache
    _sync_key_path_from_root_facade()
    provider = rsa_key_provider()
    previous_kid = _RSA_KEY_PATH.read_text().strip() if _RSA_KEY_PATH.exists() else ""
    try:
        existing_keys = (await provider.jwks()).get("keys", [])
    except Exception:
        existing_keys = []
    for item in existing_keys:
        if (
            isinstance(item, dict)
            and item.get("kid")
            and item not in _rotation_jwks_cache
        ):
            _rotation_jwks_cache.append(item)
    if previous_kid and all(
        item.get("kid") != previous_kid for item in _rotation_jwks_cache
    ):
        try:
            previous = await provider.get_public_jwk(previous_kid)
        except Exception:
            previous = {"kid": previous_kid, "kty": "RSA"}
        _rotation_jwks_cache.append(previous)
    ref = await provider.create_key(
        KeySpec(
            klass=KeyClass.asymmetric,
            alg=KeyAlg.RSA_PSS_SHA256,
            uses=(KeyUse.SIGN, KeyUse.VERIFY),
            export_policy=ExportPolicy.SECRET_WHEN_ALLOWED,
            label=f"jwt_rs256.rotate.{secrets.token_hex(4)}",
        )
    )
    _RSA_KEY_PATH.parent.mkdir(parents=True, exist_ok=True)
    _RSA_KEY_PATH.write_text(ref.kid)
    _service_cache = None
    return ref.kid


def rotation_jwks_cache() -> list[dict[str, Any]]:
    _sync_key_path_from_root_facade()
    return [dict(item) for item in _rotation_jwks_cache]


__all__ = [
    "_RSA_KEY_PATH",
    "ensure_rsa_jwt_key",
    "id_token_service",
    "rsa_key_provider",
    "rotate_rsa_jwt_key",
    "rotation_jwks_cache",
]
