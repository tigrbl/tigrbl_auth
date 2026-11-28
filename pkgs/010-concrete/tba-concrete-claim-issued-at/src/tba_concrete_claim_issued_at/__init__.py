from tba_bases_claim import ClaimBase
from tba_primitives_identity import ClaimType, ClaimValueType


class IssuedAtClaim(ClaimBase):
    claim_name = "iat"
    default_claim_type = ClaimType.PROTOCOL
    default_value_type = ClaimValueType.TIMESTAMP
    default_standards = ("RFC 7519",)

    @classmethod
    def validate_value(cls, value):
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError("iat must be a NumericDate")


__all__ = ["IssuedAtClaim"]
