from tigrbl_claim_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType


class AuthorizedPartyClaim(ClaimBase):
    claim_name = "azp"
    default_claim_type = ClaimType.AUTHORIZATION
    default_value_type = ClaimValueType.STRING
    default_standards = ("OIDC Core 1.0",)

    @classmethod
    def validate_value(cls, value):
        if not isinstance(value, str) or not value:
            raise ValueError("azp must be a non-empty string")


__all__ = ["AuthorizedPartyClaim"]
