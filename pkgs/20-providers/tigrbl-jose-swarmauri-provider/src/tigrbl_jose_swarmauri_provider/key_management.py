"""Password hashing and JWT signing key helpers.

This module keeps runtime-only framework imports lazy so repository tooling and
operator-plane services remain importable in minimal checkpoint environments.
"""

from __future__ import annotations

import asyncio
import json
import os
import pathlib
from functools import lru_cache
from typing import Any, Tuple
from uuid import uuid4

from .pqc import (
    ML_DSA_65_ALG,
    generate_pqc_signature_keypair,
    pqc_public_jwk,
    pqc_signing_jwk,
    public_key_from_pqc_jwk,
    secret_key_from_pqc_jwk,
)

_DEFAULT_KEY_DIR = pathlib.Path(os.getenv("JWT_ED25519_KEY_DIR", "runtime_secrets"))
_DEFAULT_KEY_PATH = _DEFAULT_KEY_DIR / "jwt_ed25519.kid"
_DEFAULT_PQC_KEY_PATH = pathlib.Path(
    os.getenv("JWT_ML_DSA_65_KEY_PATH", str(_DEFAULT_KEY_DIR / "jwt_ml_dsa_65.json"))
)


def _load_framework() -> dict[str, Any]:
    try:
        from swarmauri_core.crypto.types import ExportPolicy, KeyUse
        from swarmauri_core.key_providers.types import KeyAlg, KeyClass, KeySpec
        from swarmauri_keyprovider_file import FileKeyProvider
    except Exception as exc:  # pragma: no cover - environment specific
        raise RuntimeError(
            "runtime key-management dependencies are unavailable"
        ) from exc
    return {
        "ExportPolicy": ExportPolicy,
        "FileKeyProvider": FileKeyProvider,
        "KeyAlg": KeyAlg,
        "KeyClass": KeyClass,
        "KeySpec": KeySpec,
        "KeyUse": KeyUse,
    }


@lru_cache(maxsize=1)
def _provider():
    framework = _load_framework()
    provider_cls = framework["FileKeyProvider"]
    return provider_cls(_DEFAULT_KEY_DIR)


async def _create_key(label: str) -> Any:
    framework = _load_framework()
    provider = _provider()
    spec = framework["KeySpec"](
        klass=framework["KeyClass"].asymmetric,
        alg=framework["KeyAlg"].ED25519,
        uses=(framework["KeyUse"].SIGN, framework["KeyUse"].VERIFY),
        export_policy=framework["ExportPolicy"].SECRET_WHEN_ALLOWED,
        label=label,
    )
    return await provider.create_key(spec)


async def _create_and_persist_key(label: str = "jwt_ed25519") -> Any:
    ref = await _create_key(label)
    _DEFAULT_KEY_PATH.parent.mkdir(parents=True, exist_ok=True)
    _DEFAULT_KEY_PATH.write_text(ref.kid)
    return ref


async def _ensure_key() -> Tuple[str, bytes, bytes]:
    provider = _provider()
    if _DEFAULT_KEY_PATH.exists():
        kid = _DEFAULT_KEY_PATH.read_text().strip()
        if kid:
            try:
                ref = await provider.get_key(kid, include_secret=True)
            except Exception:
                ref = await _create_and_persist_key()
        else:
            ref = await _create_and_persist_key()
    else:
        ref = await _create_and_persist_key()
    return ref.kid, ref.material or b"", ref.public or b""


@lru_cache(maxsize=1)
def _load_keypair() -> Tuple[str, bytes, bytes]:
    return asyncio.run(_ensure_key())


def _generate_keypair(path: pathlib.Path) -> Tuple[str, bytes, bytes]:
    async def _create() -> Tuple[str, bytes, bytes]:
        ref = await _create_key(path.stem)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(ref.kid)
        return ref.kid, ref.material or b"", ref.public or b""

    return asyncio.run(_create())


def signing_key() -> bytes:
    return _load_keypair()[1]


def public_key() -> bytes:
    return _load_keypair()[2]


async def rotate_ed25519_jwt_key() -> str:
    ref = await _create_key("jwt_ed25519")
    _DEFAULT_KEY_PATH.parent.mkdir(parents=True, exist_ok=True)
    _DEFAULT_KEY_PATH.write_text(ref.kid)
    _load_keypair.cache_clear()
    return ref.kid


def _read_pqc_jwk(path: pathlib.Path) -> dict[str, str] | None:
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    if not isinstance(payload, dict):
        return None
    try:
        public_key_from_pqc_jwk(payload)
        secret_key_from_pqc_jwk(payload)
    except Exception:
        return None
    return {
        str(key): str(value) for key, value in payload.items() if isinstance(value, str)
    }


def _write_pqc_jwk(path: pathlib.Path, jwk: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(jwk, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def generate_pqc_jwt_keypair(*, path: pathlib.Path | None = None) -> dict[str, str]:
    target = path or _DEFAULT_PQC_KEY_PATH
    keypair = generate_pqc_signature_keypair()
    kid = f"jwt:{ML_DSA_65_ALG.lower()}:{uuid4()}"
    jwk = pqc_signing_jwk(keypair.secret_key, keypair.public_key, kid=kid)
    _write_pqc_jwk(target, jwk)
    return jwk


def ensure_pqc_keypair(*, path: pathlib.Path | None = None) -> dict[str, str]:
    target = path or _DEFAULT_PQC_KEY_PATH
    existing = _read_pqc_jwk(target)
    if existing is not None:
        return existing
    return generate_pqc_jwt_keypair(path=target)


def load_pqc_signing_jwk(*, path: pathlib.Path | None = None) -> dict[str, str]:
    return dict(ensure_pqc_keypair(path=path))


def load_pqc_public_jwk(*, path: pathlib.Path | None = None) -> dict[str, str]:
    signing_jwk = ensure_pqc_keypair(path=path)
    public_key = public_key_from_pqc_jwk(signing_jwk)
    return pqc_public_jwk(
        public_key,
        kid=signing_jwk.get("kid"),
        algorithm=str(signing_jwk.get("alg") or ML_DSA_65_ALG),
    )


async def rotate_pqc_jwt_key(*, path: pathlib.Path | None = None) -> str:
    jwk = generate_pqc_jwt_keypair(path=path)
    return jwk["kid"]


__all__ = [
    "_DEFAULT_PQC_KEY_PATH",
    "_DEFAULT_KEY_PATH",
    "_generate_keypair",
    "_load_keypair",
    "_provider",
    "generate_pqc_jwt_keypair",
    "ensure_pqc_keypair",
    "load_pqc_public_jwk",
    "load_pqc_signing_jwk",
    "public_key",
    "rotate_ed25519_jwt_key",
    "rotate_pqc_jwt_key",
    "signing_key",
]
