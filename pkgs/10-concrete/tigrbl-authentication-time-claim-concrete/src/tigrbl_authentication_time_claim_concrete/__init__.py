from tigrbl_identity_claims_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType


class AuthenticationTimeClaim(ClaimBase):
    claim_name = "auth_time"
    default_claim_type = ClaimType.AUTHENTICATION
    default_value_type = ClaimValueType.TIMESTAMP
    default_standards = ("OIDC Core 1.0",)

    @classmethod
    def validate_value(cls, value):
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError("auth_time must be a NumericDate")


__all__ = ["AuthenticationTimeClaim"]
