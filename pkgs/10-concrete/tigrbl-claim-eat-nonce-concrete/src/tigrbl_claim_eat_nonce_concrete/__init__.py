from tigrbl_identity_claims_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType


class EatNonceClaim(ClaimBase):
    claim_name = "eat_nonce"
    default_claim_type = ClaimType.ATTESTATION
    default_value_type = ClaimValueType.JSON_VALUE
    default_standards = ("RFC9711",)

    @classmethod
    def validate_value(cls, value):
        values = value if isinstance(value, (list, tuple)) else (value,)
        if not values or not all(isinstance(item, (str, bytes)) and item for item in values):
            raise ValueError("eat_nonce must contain one or more non-empty byte or text strings")


__all__ = ["EatNonceClaim"]
