from tigrbl_claim_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType


class HttpMethodClaim(ClaimBase):
    claim_name = "htm"
    default_claim_type = ClaimType.AUTHENTICATION
    default_value_type = ClaimValueType.STRING
    default_standards = ("RFC9449",)

    @classmethod
    def validate_value(cls, value):
        if not isinstance(value, str) or not value or value.upper() != value:
            raise ValueError("htm must be a non-empty uppercase HTTP method")


__all__ = ["HttpMethodClaim"]
