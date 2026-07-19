"""Standalone JOSE confirmation claim."""

from tigrbl_claim_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType


class ConfirmationClaim(ClaimBase):
    claim_name = "cnf"
    default_claim_type = ClaimType.AUTHORIZATION
    default_value_type = ClaimValueType.JSON_OBJECT
    default_standards = ("RFC7800", "RFC8705", "RFC9449")

    @classmethod
    def validate_value(cls, value):
        if not isinstance(value, dict) or len(value) != 1:
            raise ValueError("cnf requires exactly one confirmation member")

        method, confirmation = next(iter(value.items()))
        if method == "jwk":
            if not isinstance(confirmation, dict) or not confirmation.get("kty"):
                raise ValueError("cnf.jwk requires a public JWK object")
            if "d" in confirmation:
                raise ValueError("cnf.jwk must not contain private key material")
            return
        if method in {"jkt", "x5t#S256"}:
            if not isinstance(confirmation, str) or not confirmation:
                raise ValueError(f"cnf.{method} requires a non-empty thumbprint")
            return
        raise ValueError("unsupported JWT confirmation method")


__all__ = ["ConfirmationClaim"]