"""Digest helpers shared by identity packages."""

from __future__ import annotations

import hashlib
import hmac
from typing import Literal

DigestAlgorithm = Literal["sha256", "sha384", "sha512"]


def digest_bytes(data: bytes, algorithm: DigestAlgorithm = "sha256") -> bytes:
    try:
        return hashlib.new(algorithm, data).digest()
    except ValueError as exc:
        raise ValueError(f"unsupported digest algorithm: {algorithm}") from exc


def digest_text(value: str, algorithm: DigestAlgorithm = "sha256") -> str:
    return digest_bytes(value.encode("utf-8"), algorithm).hex()


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


__all__ = [
    "DigestAlgorithm",
    "constant_time_digest_equal",
    "digest_bytes",
    "digest_text",
    "sha256_digest",
    "sha256_text_digest",
    "token_hash",
]
