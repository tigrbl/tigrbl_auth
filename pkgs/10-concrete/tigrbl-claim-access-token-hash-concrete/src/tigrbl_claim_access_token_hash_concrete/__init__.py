from tigrbl_identity_claims_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType


class AccessTokenHashClaim(ClaimBase):
    claim_name = "ath"
    default_claim_type = ClaimType.AUTHENTICATION
    default_value_type = ClaimValueType.STRING
    default_standards = ("RFC9449",)

    @classmethod
    def validate_value(cls, value):
        if not isinstance(value, str) or not value:
            raise ValueError("ath must be a non-empty base64url digest")


__all__ = ["AccessTokenHashClaim"]
