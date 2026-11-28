from collections.abc import Sequence

AMR_VALUES = frozenset(
    {
        "face",
        "fpt",
        "geo",
        "hwk",
        "iris",
        "kba",
        "mca",
        "mfa",
        "otp",
        "pin",
        "pop",
        "pwd",
        "rba",
        "retina",
        "sc",
        "sms",
        "swk",
        "tel",
        "user",
        "vbm",
        "wia",
    }
)


def validate_amr_claim(amr: Sequence[str]) -> bool:
    return bool(amr) and all(
        isinstance(value, str) and value in AMR_VALUES for value in amr
    )


__all__ = ["AMR_VALUES", "validate_amr_claim"]
