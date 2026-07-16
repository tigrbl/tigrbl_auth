from tigrbl_claim_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType


class EatSubmodulesClaim(ClaimBase):
    claim_name = "submods"
    default_claim_type = ClaimType.ATTESTATION
    default_value_type = ClaimValueType.JSON_OBJECT
    default_standards = ("RFC9711",)

    @classmethod
    def validate_value(cls, value):
        if not isinstance(value, dict) or not all(isinstance(key, str) and key for key in value):
            raise ValueError("submods must be an object with non-empty string names")


__all__ = ["EatSubmodulesClaim"]
