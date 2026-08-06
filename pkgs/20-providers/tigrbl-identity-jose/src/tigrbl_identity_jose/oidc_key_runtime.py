"""Internal RSA signing-key lifecycle for OIDC ID Tokens."""
from __future__ import annotations

import os
import pathlib
import secrets
import sys
from functools import lru_cache
from typing import Any

from .framework import ExportPolicy, FileKeyProvider, JWTTokenService, KeyAlg, KeyClass, KeySpec, KeyUse

_RSA_KEY_PATH = pathlib.Path(os.getenv("JWT_RS256_KEY_PATH", "runtime_secrets/jwt_rs256.kid"))
_service_cache: tuple[JWTTokenService, str] | None = None
_rotation_jwks_cache: list[dict[str, Any]] = []

def _sync_key_path_from_root_facade() -> None:
    global _RSA_KEY_PATH, _service_cache
    facade = sys.modules.get("tigrbl_auth.oidc_id_token")
    root_path = getattr(facade, "_RSA_KEY_PATH", None)
    if root_path is None or pathlib.Path(root_path) == _RSA_KEY_PATH: return
    _RSA_KEY_PATH = pathlib.Path(root_path); _service_cache = None; rsa_key_provider.cache_clear()

@lru_cache(maxsize=1)
def rsa_key_provider() -> FileKeyProvider: return FileKeyProvider(_RSA_KEY_PATH.parent)

async def _create_rsa_key():
    ref = await rsa_key_provider().create_key(KeySpec(KeyClass.asymmetric, KeyAlg.RSA_PSS_SHA256, (KeyUse.SIGN, KeyUse.VERIFY), ExportPolicy.SECRET_WHEN_ALLOWED, "jwt_rs256"))
    _RSA_KEY_PATH.parent.mkdir(parents=True, exist_ok=True); _RSA_KEY_PATH.write_text(ref.kid, encoding="utf-8")
    return ref

async def ensure_rsa_jwt_key() -> tuple[str, bytes, bytes]:
    _sync_key_path_from_root_facade(); ref = None
    if _RSA_KEY_PATH.exists():
        kid = _RSA_KEY_PATH.read_text(encoding="utf-8").strip()
        if kid:
            try: ref = await rsa_key_provider().get_key(kid, include_secret=True)
            except Exception: pass
    if ref is None: ref = await _create_rsa_key()
    return ref.kid, ref.material or b"", ref.public or b""

async def id_token_service() -> tuple[JWTTokenService, str]:
    global _service_cache
    if _service_cache is None:
        kid, _, _ = await ensure_rsa_jwt_key(); _service_cache = (JWTTokenService(rsa_key_provider()), kid)
    return _service_cache

async def rotate_rsa_jwt_key() -> str:
    global _service_cache
    _sync_key_path_from_root_facade(); provider = rsa_key_provider()
    previous = _RSA_KEY_PATH.read_text(encoding="utf-8").strip() if _RSA_KEY_PATH.exists() else ""
    if previous:
        try: old = await provider.get_public_jwk(previous)
        except Exception: old = {"kid": previous, "kty": "RSA"}
        if old not in _rotation_jwks_cache: _rotation_jwks_cache.append(old)
    ref = await provider.create_key(KeySpec(KeyClass.asymmetric, KeyAlg.RSA_PSS_SHA256, (KeyUse.SIGN, KeyUse.VERIFY), ExportPolicy.SECRET_WHEN_ALLOWED, f"jwt_rs256.rotate.{secrets.token_hex(4)}"))
    _RSA_KEY_PATH.parent.mkdir(parents=True, exist_ok=True); _RSA_KEY_PATH.write_text(ref.kid, encoding="utf-8"); _service_cache = None
    return ref.kid

def rotation_jwks_cache() -> list[dict[str, Any]]: _sync_key_path_from_root_facade(); return [dict(item) for item in _rotation_jwks_cache]

__all__ = ["_RSA_KEY_PATH", "ensure_rsa_jwt_key", "id_token_service", "rsa_key_provider", "rotate_rsa_jwt_key", "rotation_jwks_cache"]
