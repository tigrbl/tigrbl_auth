from tigrbl_identity_claims_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType


class SubjectClaim(ClaimBase):
    claim_name = "sub"
    default_claim_type = ClaimType.IDENTITY
    default_value_type = ClaimValueType.STRING
    default_standards = ("RFC 7519", "OIDC Core 1.0")

    @classmethod
    def validate_value(cls, value):
        if not isinstance(value, str) or not value:
            raise ValueError("sub must be a non-empty string")


__all__ = ["SubjectClaim"]
