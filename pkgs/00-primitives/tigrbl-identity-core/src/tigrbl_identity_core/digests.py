"""Digest helpers shared by identity packages."""

from __future__ import annotations

import hashlib
import hmac


def sha256_text_digest(value: str) -> str:
    """Return the SHA-256 hex digest of UTF-8 text."""

    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def token_hash(token: object) -> str:
    """Return the stable token/storage identifier digest for a token-like value."""

    return sha256_text_digest(str(token))


def sha256_digest(value: bytes) -> bytes:
    """Return the raw SHA-256 digest of bytes."""

    return hashlib.sha256(value).digest()


def constant_time_digest_equal(left: bytes, right: bytes) -> bool:
    """Compare digests without data-dependent early exit."""

    return hmac.compare_digest(left, right)


__all__ = ["constant_time_digest_equal", "sha256_digest", "sha256_text_digest", "token_hash"]
