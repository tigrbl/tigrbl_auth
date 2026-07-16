from tigrbl_claim_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType


class AuthenticationMethodsClaim(ClaimBase):
    claim_name = "amr"
    default_claim_type = ClaimType.AUTHENTICATION
    default_value_type = ClaimValueType.STRING_LIST
    default_standards = ("RFC 8176", "OIDC Core 1.0")

    @classmethod
    def validate_value(cls, value):
        if (
            not isinstance(value, (list, tuple))
            or not value
            or not all(isinstance(v, str) and v for v in value)
        ):
            raise ValueError("amr must be a non-empty string list")


__all__ = ["AuthenticationMethodsClaim"]
