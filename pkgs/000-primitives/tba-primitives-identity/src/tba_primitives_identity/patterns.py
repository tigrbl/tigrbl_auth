"""Pattern matching helpers shared by identity packages."""

from __future__ import annotations


def matches_dotted_pattern(pattern: str, value: str) -> bool:
    """Match exact, wildcard, or dotted-prefix patterns."""

    if pattern == "*" or pattern == value:
        return True
    if pattern.endswith(".*"):
        prefix = pattern[:-2]
        return value == prefix or value.startswith(f"{prefix}.")
    return False


__all__ = ["matches_dotted_pattern"]
