from tigrbl_claim_bases import ClaimBase
from tigrbl_identity_core import ClaimNameKind, ClaimType, ClaimValueType


class CwtIssuedAtClaim(ClaimBase):
    claim_name = 6
    default_name_kind = ClaimNameKind.INTEGER_LABEL
    default_registry = "IANA CWT Claims"
    default_claim_type = ClaimType.PROTOCOL
    default_value_type = ClaimValueType.TIMESTAMP
    default_standards = ("RFC8392",)

    @classmethod
    def validate_value(cls, value):
        if not (isinstance(value, int) and not isinstance(value, bool)):
            raise ValueError("CWT claim 6 has an invalid value")


__all__ = ["CwtIssuedAtClaim"]
