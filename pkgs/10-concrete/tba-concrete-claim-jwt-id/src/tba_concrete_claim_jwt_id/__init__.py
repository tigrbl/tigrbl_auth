from tba_bases_claim import ClaimBase
from tba_primitives_identity import ClaimType, ClaimValueType


class JwtIdClaim(ClaimBase):
    claim_name = "jti"
    default_claim_type = ClaimType.TRANSACTION
    default_value_type = ClaimValueType.STRING
    default_standards = ("RFC 7519",)

    @classmethod
    def validate_value(cls, value):
        if not isinstance(value, str) or not value:
            raise ValueError("jti must be a non-empty string")


__all__ = ["JwtIdClaim"]
