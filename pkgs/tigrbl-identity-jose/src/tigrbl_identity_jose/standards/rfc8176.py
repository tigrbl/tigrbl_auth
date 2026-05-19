"""Authentication Method Reference utilities for RFC 8176 compliance."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Final

from tigrbl_auth.config.settings import settings

RFC8176_SPEC_URL: Final[str] = "https://www.rfc-editor.org/rfc/rfc8176"
AMR_VALUES: set[str] = {
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


def validate_amr_claim(amr: Sequence[str], *, enabled: bool | None = None) -> bool:
    if enabled is None:
        enabled = settings.enable_rfc8176
    if not enabled:
        return True
    return all(value in AMR_VALUES for value in amr)


__all__ = ["RFC8176_SPEC_URL", "AMR_VALUES", "validate_amr_claim"]
