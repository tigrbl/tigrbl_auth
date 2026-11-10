"""Time-based one-time passwords (RFC 6238)."""

import hmac

from .hotp import hotp


def time_step(timestamp: int, *, period: int = 30) -> int:
    if type(timestamp) is not int or timestamp < 0:
        raise ValueError("Use a non-negative Unix timestamp in seconds.")
    if type(period) is not int or period <= 0:
        raise ValueError("The period must be a positive integer.")
    return timestamp // period


def match_step(
    key: bytes,
    code: str,
    timestamp: int,
    *,
    digits: int = 6,
    algorithm: str = "sha1",
    period: int = 30,
    window: int = 0,
    after_step: int = -1,
) -> int | None:
    """Return the first matching step newer than the caller's replay cursor."""
    current = time_step(timestamp, period=period)
    if type(window) is not int or not 0 <= window <= 2:
        raise ValueError("The drift window must be between zero and two steps.")
    if not isinstance(code, str) or len(code) != digits or not code.isascii() or not code.isdigit():
        return None

    offsets = [0]
    for offset in range(1, window + 1):
        offsets.extend((-offset, offset))
    for offset in offsets:
        step = current + offset
        if 0 <= step < 2**64 and step > after_step:
            expected = hotp(key, step, digits=digits, algorithm=algorithm)
            if hmac.compare_digest(expected, code):
                return step
    return None
