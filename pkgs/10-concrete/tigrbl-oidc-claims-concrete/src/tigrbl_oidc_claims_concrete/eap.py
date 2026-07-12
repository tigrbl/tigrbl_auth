"""OpenID Connect EAP ACR Values 1.0 (Final, June 2025)."""

from __future__ import annotations

from enum import StrEnum
from typing import Iterable

SPEC_URL = "https://openid.net/specs/openid-connect-eap-acr-values-1_0-final.html"


class EapAcrValue(StrEnum):
    PHISHING_RESISTANT = "phr"
    PHISHING_RESISTANT_HARDWARE = "phrh"


class EapAmrValue(StrEnum):
    PROOF_OF_POSSESSION = "pop"


def satisfies_eap_acr(*, requested: str, achieved: Iterable[str]) -> bool:
    """Return whether achieved authentication contexts satisfy the request."""
    values = set(achieved)
    if requested == EapAcrValue.PHISHING_RESISTANT:
        return bool(values & {EapAcrValue.PHISHING_RESISTANT, EapAcrValue.PHISHING_RESISTANT_HARDWARE})
    if requested == EapAcrValue.PHISHING_RESISTANT_HARDWARE:
        return EapAcrValue.PHISHING_RESISTANT_HARDWARE in values
    return requested in values


__all__ = ["EapAcrValue", "EapAmrValue", "SPEC_URL", "satisfies_eap_acr"]
