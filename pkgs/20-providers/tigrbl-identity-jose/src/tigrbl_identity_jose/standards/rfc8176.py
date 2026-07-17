"""Authentication Method Reference utilities for RFC 8176 compliance."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Final

from tigrbl_jose_concrete import AMR_VALUES, validate_amr_claim as _validate_amr_claim
from ..configuration import settings

RFC8176_SPEC_URL: Final[str] = "https://www.rfc-editor.org/rfc/rfc8176"


def validate_amr_claim(amr: Sequence[str], *, enabled: bool | None = None) -> bool:
    if enabled is None:
        enabled = settings.enable_rfc8176
    if not enabled:
        return True
    return _validate_amr_claim(amr)


__all__ = ["RFC8176_SPEC_URL", "AMR_VALUES", "validate_amr_claim"]
