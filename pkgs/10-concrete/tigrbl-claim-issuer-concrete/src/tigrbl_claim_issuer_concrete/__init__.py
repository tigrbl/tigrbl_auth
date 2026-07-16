from tigrbl_claim_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType


class IssuerClaim(ClaimBase):
    claim_name = "iss"
    default_claim_type = ClaimType.PROTOCOL
    default_value_type = ClaimValueType.URI
    default_standards = ("RFC 7519",)

    @classmethod
    def validate_value(cls, value):
        if not isinstance(value, str) or not value:
            raise ValueError("iss must be a non-empty string")


__all__ = ["IssuerClaim"]
