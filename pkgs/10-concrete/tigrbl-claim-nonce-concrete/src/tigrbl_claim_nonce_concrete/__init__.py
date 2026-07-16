from tigrbl_claim_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType


class NonceClaim(ClaimBase):
    claim_name = "nonce"
    default_claim_type = ClaimType.TRANSACTION
    default_value_type = ClaimValueType.STRING
    default_standards = ("OIDC Core 1.0", "RFC 9449", "RFC 9711")

    @classmethod
    def validate_value(cls, value):
        if not isinstance(value, str) or not value:
            raise ValueError("nonce must be a non-empty string")


__all__ = ["NonceClaim"]
