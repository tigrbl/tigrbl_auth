from tigrbl_claim_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType


class NotBeforeClaim(ClaimBase):
    claim_name = "nbf"
    default_claim_type = ClaimType.PROTOCOL
    default_value_type = ClaimValueType.TIMESTAMP
    default_standards = ("RFC 7519",)

    @classmethod
    def validate_value(cls, value):
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError("nbf must be a NumericDate")


__all__ = ["NotBeforeClaim"]
