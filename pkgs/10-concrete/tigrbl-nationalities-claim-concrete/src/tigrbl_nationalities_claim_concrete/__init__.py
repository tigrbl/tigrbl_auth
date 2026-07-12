from tigrbl_identity_claims_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType


class NationalitiesClaim(ClaimBase):
    claim_name = "nationalities"
    default_claim_type = ClaimType.IDENTITY
    default_value_type = ClaimValueType.STRING_LIST
    default_standards = ("OpenID Identity Assurance 1.0",)

    @classmethod
    def validate_value(cls, value):
        if (
            not isinstance(value, (list, tuple))
            or not value
            or not all(isinstance(item, str) and item for item in value)
        ):
            raise ValueError("nationalities must be a non-empty string array")


__all__ = ["NationalitiesClaim"]
