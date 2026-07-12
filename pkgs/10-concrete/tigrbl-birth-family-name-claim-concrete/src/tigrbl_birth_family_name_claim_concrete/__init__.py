from tigrbl_identity_claims_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType


class BirthFamilyNameClaim(ClaimBase):
    claim_name = "birth_family_name"
    default_claim_type = ClaimType.IDENTITY
    default_value_type = ClaimValueType.STRING
    default_standards = ("OpenID Identity Assurance 1.0",)

    @classmethod
    def validate_value(cls, value):
        if not isinstance(value, str) or not value:
            raise ValueError("birth_family_name must be a non-empty string")


__all__ = ["BirthFamilyNameClaim"]
