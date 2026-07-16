from tigrbl_claim_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType


class AudienceClaim(ClaimBase):
    claim_name = "aud"
    default_claim_type = ClaimType.PROTOCOL
    default_value_type = ClaimValueType.JSON_VALUE
    default_standards = ("RFC 7519",)

    @classmethod
    def validate_value(cls, value):
        if not (
            isinstance(value, str)
            and value
            or isinstance(value, (list, tuple))
            and value
            and all(isinstance(v, str) and v for v in value)
        ):
            raise ValueError("aud must be a string or non-empty string list")


__all__ = ["AudienceClaim"]
