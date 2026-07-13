from tigrbl_identity_claims_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType


class AlsoKnownAsClaim(ClaimBase):
    claim_name = "also_known_as"
    default_claim_type = ClaimType.IDENTITY
    default_value_type = ClaimValueType.STRING
    default_standards = ("OpenID Identity Assurance 1.0",)

    @classmethod
    def validate_value(cls, value):
        if not isinstance(value, str) or not value:
            raise ValueError("also_known_as must be a non-empty string")


__all__ = ["AlsoKnownAsClaim"]
