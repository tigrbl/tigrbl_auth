"""HMAC-based one-time passwords (RFC 4226)."""

import hmac


def hotp(
    key: bytes, counter: int, *, digits: int = 6, algorithm: str = "sha1"
) -> str:
    if not isinstance(key, bytes) or not key:
        raise ValueError("An HMAC key is required.")
    if type(counter) is not int or not 0 <= counter < 2**64:
        raise ValueError("The counter must be an unsigned 64-bit integer.")
    if type(digits) is not int or digits not in (6, 7, 8):
        raise ValueError("Use six, seven, or eight digits.")
    if algorithm not in ("sha1", "sha256", "sha512"):
        raise ValueError("Unsupported HMAC algorithm.")
    digest = hmac.digest(key, counter.to_bytes(8, "big"), algorithm)
    offset = digest[-1] & 0x0F
    number = int.from_bytes(digest[offset : offset + 4], "big") & 0x7FFFFFFF
    return str(number % 10**digits).zfill(digits)
