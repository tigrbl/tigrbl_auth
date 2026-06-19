"""Minimal operator password hashing helper."""

from __future__ import annotations

import hashlib

try:  # pragma: no cover - optional in minimal environments
    import bcrypt
except Exception:  # pragma: no cover
    bcrypt = None

_BCRYPT_ROUNDS = 12
_BCRYPT_MAX_BYTES = 72


def _bcrypt_bytes(plain: str) -> bytes:
    data = plain.encode()
    return data[:_BCRYPT_MAX_BYTES] if len(data) > _BCRYPT_MAX_BYTES else data


def hash_pw(plain: str) -> bytes:
    if bcrypt is None:
        return hashlib.sha256(_bcrypt_bytes(plain)).hexdigest().encode("utf-8")
    return bcrypt.hashpw(_bcrypt_bytes(plain), bcrypt.gensalt(_BCRYPT_ROUNDS))


__all__ = ["hash_pw"]
