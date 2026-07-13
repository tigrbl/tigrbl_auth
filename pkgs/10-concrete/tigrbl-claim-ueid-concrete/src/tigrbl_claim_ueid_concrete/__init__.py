from tigrbl_identity_claims_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType


class UeidClaim(ClaimBase):
    claim_name = "ueid"
    default_claim_type = ClaimType.ATTESTATION
    default_value_type = ClaimValueType.JSON_VALUE
    default_standards = ("RFC9711",)

    @classmethod
    def validate_value(cls, value):
        if not isinstance(value, (str, bytes)) or not value:
            raise ValueError("ueid must be a non-empty byte or text string")


__all__ = ["UeidClaim"]
