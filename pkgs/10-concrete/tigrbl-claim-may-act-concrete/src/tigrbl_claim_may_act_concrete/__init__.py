from tigrbl_claim_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType


class MayActClaim(ClaimBase):
    claim_name = "may_act"
    default_claim_type = ClaimType.AUTHORIZATION
    default_value_type = ClaimValueType.JSON_OBJECT
    default_standards = ("RFC8693",)

    @classmethod
    def validate_value(cls, value):
        if not isinstance(value, dict) or not value:
            raise ValueError("may_act must be a non-empty JSON object")


__all__ = ["MayActClaim"]
