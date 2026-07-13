from tigrbl_identity_claims_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType


class SdHashClaim(ClaimBase):
    claim_name = "sd_hash"
    default_claim_type = ClaimType.CREDENTIAL
    default_value_type = ClaimValueType.STRING
    default_standards = ("SD-JWT",)

    @classmethod
    def validate_value(cls, value):
        if not isinstance(value, str) or not value:
            raise ValueError("sd_hash must be a non-empty base64url digest")


__all__ = ["SdHashClaim"]
