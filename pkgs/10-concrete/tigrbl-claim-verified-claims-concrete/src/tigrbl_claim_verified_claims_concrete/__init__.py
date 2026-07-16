from tigrbl_claim_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType


class VerifiedClaimsClaim(ClaimBase):
    claim_name = "verified_claims"
    default_claim_type = ClaimType.ASSURANCE
    default_value_type = ClaimValueType.JSON_OBJECT
    default_standards = ("OpenID Identity Assurance Schema Definition 1.0",)

    @classmethod
    def validate_value(cls, value):
        if (
            not isinstance(value, dict)
            or not isinstance(value.get("verification"), dict)
            or not isinstance(value.get("claims"), dict)
        ):
            raise ValueError("verified_claims requires verification and claims objects")


__all__ = ["VerifiedClaimsClaim"]
