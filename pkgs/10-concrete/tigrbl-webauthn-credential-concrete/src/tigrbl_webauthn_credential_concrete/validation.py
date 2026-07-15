"""Validation helpers for registered WebAuthn credential values."""


def validate_cose_algorithm(value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("COSE algorithm identifier must be an integer")
    return value


__all__ = ["validate_cose_algorithm"]
