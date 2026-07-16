from tigrbl_claim_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType


class ScopeClaim(ClaimBase):
    claim_name = "scope"
    default_claim_type = ClaimType.AUTHORIZATION
    default_value_type = ClaimValueType.STRING
    default_standards = ("RFC 8693", "RFC 9068")

    @classmethod
    def validate_value(cls, value):
        if not isinstance(value, str) or any(not item for item in value.split(" ")):
            raise ValueError("scope must be a space-delimited string")


__all__ = ["ScopeClaim"]
