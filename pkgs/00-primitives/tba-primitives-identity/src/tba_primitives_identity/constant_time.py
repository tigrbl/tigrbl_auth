"""Constant-time comparisons for secret-adjacent byte and text values."""

from __future__ import annotations
import hmac


def bytes_equal(left: bytes, right: bytes) -> bool:
    return hmac.compare_digest(left, right)


def text_equal(left: str, right: str) -> bool:
    return hmac.compare_digest(left.encode(), right.encode())


__all__ = ["bytes_equal", "text_equal"]
