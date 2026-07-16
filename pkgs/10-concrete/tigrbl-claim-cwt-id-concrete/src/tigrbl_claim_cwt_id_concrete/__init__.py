from tigrbl_claim_bases import ClaimBase
from tigrbl_identity_core import ClaimNameKind, ClaimType, ClaimValueType


class CwtIdClaim(ClaimBase):
    claim_name = 7
    default_name_kind = ClaimNameKind.INTEGER_LABEL
    default_registry = "IANA CWT Claims"
    default_claim_type = ClaimType.TRANSACTION
    default_value_type = ClaimValueType.BYTES
    default_standards = ("RFC8392",)

    @classmethod
    def validate_value(cls, value):
        if not (isinstance(value, bytes) and bool(value)):
            raise ValueError("CWT claim 7 has an invalid value")


__all__ = ["CwtIdClaim"]
