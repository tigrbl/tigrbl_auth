"""Durable signing-key management owned by Tigrbl Auth."""

from __future__ import annotations

import asyncio
import json
import os
import pathlib
from functools import lru_cache
from typing import Any
from uuid import uuid4

from tigrbl_secret_hashing_bcrypt_provider import hash_pw, verify_pw

from .framework import ExportPolicy, FileKeyProvider, KeyAlg, KeyClass, KeySpec, KeyUse
from .pqc import (
    ML_DSA_65_ALG, generate_pqc_signature_keypair, pqc_public_jwk,
    pqc_signing_jwk, public_key_from_pqc_jwk, secret_key_from_pqc_jwk,
)

_DEFAULT_KEY_DIR = pathlib.Path(os.getenv("JWT_ED25519_KEY_DIR", "runtime_secrets"))
_DEFAULT_KEY_PATH = _DEFAULT_KEY_DIR / "jwt_ed25519.kid"
_DEFAULT_PQC_KEY_PATH = pathlib.Path(os.getenv("JWT_ML_DSA_65_KEY_PATH", str(_DEFAULT_KEY_DIR / "jwt_ml_dsa_65.json")))


@lru_cache(maxsize=1)
def _provider() -> FileKeyProvider:
    return FileKeyProvider(_DEFAULT_KEY_DIR)


async def _create_key(label: str) -> Any:
    return await _provider().create_key(KeySpec(KeyClass.asymmetric, KeyAlg.ED25519, (KeyUse.SIGN, KeyUse.VERIFY), ExportPolicy.SECRET_WHEN_ALLOWED, label))


async def _create_and_persist_key(label: str = "jwt_ed25519") -> Any:
    ref = await _create_key(label)
    _DEFAULT_KEY_PATH.parent.mkdir(parents=True, exist_ok=True)
    _DEFAULT_KEY_PATH.write_text(ref.kid, encoding="utf-8")
    try: os.chmod(_DEFAULT_KEY_PATH, 0o600)
    except OSError: pass
    return ref


async def _ensure_key() -> tuple[str, bytes, bytes]:
    ref = None
    if _DEFAULT_KEY_PATH.exists():
        kid = _DEFAULT_KEY_PATH.read_text(encoding="utf-8").strip()
        if kid:
            try: ref = await _provider().get_key(kid, include_secret=True)
            except Exception: pass
    if ref is None:
        ref = await _create_and_persist_key()
    if ref.tags.get("alg") != KeyAlg.ED25519.value:
        raise RuntimeError("JWT signing key is not Ed25519")
    return ref.kid, ref.material or b"", ref.public or b""


@lru_cache(maxsize=1)
def _load_keypair() -> tuple[str, bytes, bytes]:
    return asyncio.run(_ensure_key())


def _generate_keypair(path: pathlib.Path) -> tuple[str, bytes, bytes]:
    async def create() -> tuple[str, bytes, bytes]:
        ref = await _create_key(path.stem)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(ref.kid, encoding="utf-8")
        try: os.chmod(path, 0o600)
        except OSError: pass
        return ref.kid, ref.material or b"", ref.public or b""
    return asyncio.run(create())


def signing_key() -> bytes: return _load_keypair()[1]
def public_key() -> bytes: return _load_keypair()[2]


async def rotate_ed25519_jwt_key() -> str:
    ref = await _create_and_persist_key()
    _load_keypair.cache_clear()
    return ref.kid


def _read_pqc_jwk(path: pathlib.Path) -> dict[str, str] | None:
    try: payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception: return None
    if not isinstance(payload, dict): return None
    try: public_key_from_pqc_jwk(payload); secret_key_from_pqc_jwk(payload)
    except Exception: return None
    return {str(k): str(v) for k, v in payload.items() if isinstance(v, str)}


def _write_pqc_jwk(path: pathlib.Path, jwk: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(jwk, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def generate_pqc_jwt_keypair(*, path: pathlib.Path | None = None) -> dict[str, str]:
    target = path or _DEFAULT_PQC_KEY_PATH
    pair = generate_pqc_signature_keypair()
    jwk = pqc_signing_jwk(pair.secret_key, pair.public_key, kid=f"jwt:{ML_DSA_65_ALG.lower()}:{uuid4()}")
    _write_pqc_jwk(target, jwk)
    return jwk


def ensure_pqc_keypair(*, path: pathlib.Path | None = None) -> dict[str, str]:
    target = path or _DEFAULT_PQC_KEY_PATH
    return _read_pqc_jwk(target) or generate_pqc_jwt_keypair(path=target)


def load_pqc_signing_jwk(*, path: pathlib.Path | None = None) -> dict[str, str]: return dict(ensure_pqc_keypair(path=path))
def load_pqc_public_jwk(*, path: pathlib.Path | None = None) -> dict[str, str]:
    jwk = ensure_pqc_keypair(path=path)
    return pqc_public_jwk(public_key_from_pqc_jwk(jwk), kid=jwk.get("kid"), algorithm=str(jwk.get("alg") or ML_DSA_65_ALG))
async def rotate_pqc_jwt_key(*, path: pathlib.Path | None = None) -> str: return generate_pqc_jwt_keypair(path=path)["kid"]


__all__ = ["ExportPolicy", "FileKeyProvider", "KeyAlg", "KeyClass", "KeySpec", "KeyUse", "_DEFAULT_KEY_PATH", "_DEFAULT_PQC_KEY_PATH", "_ensure_key", "_generate_keypair", "_load_keypair", "_provider", "ensure_pqc_keypair", "generate_pqc_jwt_keypair", "hash_pw", "load_pqc_public_jwk", "load_pqc_signing_jwk", "public_key", "rotate_ed25519_jwt_key", "rotate_pqc_jwt_key", "signing_key", "verify_pw"]
