"""OIDC EAP ACR Values 1.0 profile values and satisfaction rules."""

from __future__ import annotations

from collections.abc import Iterable

from tigrbl_identity_contracts.oidc.eap_acr import EapAcrValue, EapAmrValue

SPEC_URL = "https://openid.net/specs/openid-connect-eap-acr-values-1_0.html"


def satisfies_eap_acr(*, requested: str, achieved: Iterable[str]) -> bool:
    values = {str(value) for value in achieved}
    if requested == EapAcrValue.PHISHING_RESISTANT:
        return bool(
            values
            & {
                EapAcrValue.PHISHING_RESISTANT,
                EapAcrValue.PHISHING_RESISTANT_HARDWARE,
            }
        )
    if requested == EapAcrValue.PHISHING_RESISTANT_HARDWARE:
        return EapAcrValue.PHISHING_RESISTANT_HARDWARE in values
    return False


__all__ = ["EapAcrValue", "EapAmrValue", "SPEC_URL", "satisfies_eap_acr"]
