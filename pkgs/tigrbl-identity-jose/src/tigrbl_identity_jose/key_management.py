"""Password hashing and JWT signing key helpers.

This module keeps runtime-only framework imports lazy so repository tooling and
operator-plane services remain importable in minimal checkpoint environments.
"""

from __future__ import annotations

import asyncio
import hashlib
import os
import pathlib
from functools import lru_cache
from typing import Any, Tuple

try:  # pragma: no cover - optional in minimal environments
    import bcrypt
except Exception:  # pragma: no cover
    bcrypt = None

_DEFAULT_KEY_DIR = pathlib.Path(os.getenv("JWT_ED25519_KEY_DIR", "runtime_secrets"))
_DEFAULT_KEY_PATH = _DEFAULT_KEY_DIR / "jwt_ed25519.kid"
_BCRYPT_ROUNDS = 12
_BCRYPT_MAX_BYTES = 72


def _load_framework() -> dict[str, Any]:
    try:
        from tigrbl_auth.framework import ExportPolicy, FileKeyProvider, KeyAlg, KeyClass, KeySpec, KeyUse
    except Exception as exc:  # pragma: no cover - environment specific
        raise RuntimeError("runtime key-management dependencies are unavailable") from exc
    return {
        "ExportPolicy": ExportPolicy,
        "FileKeyProvider": FileKeyProvider,
        "KeyAlg": KeyAlg,
        "KeyClass": KeyClass,
        "KeySpec": KeySpec,
        "KeyUse": KeyUse,
    }


def _bcrypt_bytes(plain: str) -> bytes:
    data = plain.encode()
    return data[:_BCRYPT_MAX_BYTES] if len(data) > _BCRYPT_MAX_BYTES else data


def hash_pw(plain: str) -> bytes:
    if bcrypt is None:
        return hashlib.sha256(_bcrypt_bytes(plain)).hexdigest().encode("utf-8")
    return bcrypt.hashpw(_bcrypt_bytes(plain), bcrypt.gensalt(_BCRYPT_ROUNDS))


def verify_pw(plain: str, hashed: bytes) -> bool:
    if hashed is None:
        return False
    if bcrypt is None:
        return hashlib.sha256(_bcrypt_bytes(plain)).hexdigest().encode("utf-8") == hashed
    try:
        return bcrypt.checkpw(_bcrypt_bytes(plain), hashed)
    except (TypeError, ValueError):
        return False


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


# -----------------------------
# Operator-plane wrappers
# -----------------------------


def _operator_context(*, repo_root: pathlib.Path | str, command: str, profile: str | None = None, tenant: str | None = None, issuer: str | None = None, actor: str | None = None, dry_run: bool = False):
    from ._operator_store import OperationContext

    return OperationContext(
        repo_root=pathlib.Path(repo_root),
        command=command,
        resource="keys",
        dry_run=dry_run,
        actor=actor or "system",
        profile=profile,
        tenant=tenant,
        issuer=issuer,
    )


def generate_operator_key_for_context(context, *, patch: dict[str, Any] | None = None):
    from .operator_service import generate_key_record

    return generate_key_record(context, patch=patch)


def import_operator_key_for_context(context, *, patch: dict[str, Any] | None = None):
    from .operator_service import create_resource

    patch = dict(patch or {})
    record_id = str(patch.get("kid") or patch.get("id") or patch.get("name") or "imported-key")
    return create_resource(context, record_id=record_id, patch=patch, if_exists="update")


def export_operator_key_for_context(context, *, record_id: str):
    from .operator_service import get_resource

    return get_resource(context, record_id=record_id)


def rotate_operator_key_for_context(context, *, record_id: str):
    from .operator_service import rotate_key_record

    return rotate_key_record(context, record_id=record_id)


def retire_operator_key_for_context(context, *, record_id: str, retire_after: str | None = None):
    from .operator_service import retire_key_record

    return retire_key_record(context, record_id=record_id, retire_after=retire_after)


def publish_operator_jwks_for_context(context, *, output_path: str | None = None):
    from .operator_service import publish_jwks_document

    return publish_jwks_document(context, output_path=output_path)


def list_operator_keys_for_context(context, *, status_filter: str | None = None, filter_expr: str | None = None, sort: str = "id", offset: int = 0, limit: int = 50):
    from .operator_service import list_resource_result

    return list_resource_result(context, status_filter=status_filter, filter_expr=filter_expr, sort=sort, offset=offset, limit=limit)


def get_operator_key_for_context(context, *, record_id: str):
    from .operator_service import get_resource

    return get_resource(context, record_id=record_id)


def delete_operator_key_for_context(context, *, record_id: str, if_missing: str = "error"):
    from .operator_service import delete_resource

    return delete_resource(context, record_id=record_id, if_missing=if_missing)


__all__ = [
    "_DEFAULT_KEY_PATH",
    "_generate_keypair",
    "_load_keypair",
    "_provider",
    "delete_operator_key_for_context",
    "export_operator_key_for_context",
    "generate_operator_key_for_context",
    "get_operator_key_for_context",
    "hash_pw",
    "import_operator_key_for_context",
    "list_operator_keys_for_context",
    "public_key",
    "publish_operator_jwks_for_context",
    "retire_operator_key_for_context",
    "rotate_ed25519_jwt_key",
    "rotate_operator_key_for_context",
    "signing_key",
    "verify_pw",
]
