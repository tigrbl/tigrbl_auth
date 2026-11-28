"""Cryptographically secure nonce primitives."""

import hmac
import secrets

from .base64url import base64url_encode

MIN_NONCE_BYTES = 16


def generate_nonce(*, size: int = 32) -> str:
    if size < MIN_NONCE_BYTES:
        raise ValueError(f"nonce size must be at least {MIN_NONCE_BYTES} bytes")
    return base64url_encode(secrets.token_bytes(size))


def validate_nonce(value: str, *, min_length: int = 22) -> str:
    normalized = str(value).strip()
    if len(normalized) < min_length:
        raise ValueError("nonce is too short")
    return normalized


def nonce_equal(left: str, right: str) -> bool:
    return hmac.compare_digest(str(left), str(right))


__all__ = ["MIN_NONCE_BYTES", "generate_nonce", "nonce_equal", "validate_nonce"]
