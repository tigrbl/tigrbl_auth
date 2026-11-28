"""Deprecated aggregate facade for split assurance and OIDC profile owners."""

import warnings

from tigrbl_auth_protocol_oidc.eap_acr_values import (
    EapAcrValue,
    EapAmrValue,
    satisfies_eap_acr,
)
from tigrbl_identity_assurance_concrete import (
    parse_verified_claims,
    serialize_verified_claims,
)

warnings.warn(
    "tigrbl_oidc_claims_concrete is deprecated; import assurance behavior and "
    "OIDC EAP values from their standalone owners",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = [
    "EapAcrValue",
    "EapAmrValue",
    "parse_verified_claims",
    "serialize_verified_claims",
    "satisfies_eap_acr",
]
