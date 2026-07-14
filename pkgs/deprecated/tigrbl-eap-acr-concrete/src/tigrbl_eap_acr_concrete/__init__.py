"""Deprecated facade for the OIDC EAP ACR Values profile."""

import warnings

from tigrbl_auth_protocol_oidc.eap_acr_values import (
    EapAcrValue,
    EapAmrValue,
    SPEC_URL,
    satisfies_eap_acr,
)

warnings.warn(
    "tigrbl_eap_acr_concrete is deprecated; import from "
    "tigrbl_auth_protocol_oidc.eap_acr_values",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ["EapAcrValue", "EapAmrValue", "SPEC_URL", "satisfies_eap_acr"]
