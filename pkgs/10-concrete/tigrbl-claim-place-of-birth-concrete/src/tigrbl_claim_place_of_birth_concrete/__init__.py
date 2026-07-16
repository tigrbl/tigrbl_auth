from tigrbl_claim_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType


class PlaceOfBirthClaim(ClaimBase):
    claim_name = "place_of_birth"
    default_claim_type = ClaimType.IDENTITY
    default_value_type = ClaimValueType.JSON_OBJECT
    default_standards = ("OpenID Identity Assurance 1.0",)

    @classmethod
    def validate_value(cls, value):
        if not isinstance(value, dict) or not value:
            raise ValueError("place_of_birth must be a non-empty object")


__all__ = ["PlaceOfBirthClaim"]
