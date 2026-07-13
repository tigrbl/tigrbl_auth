from tigrbl_identity_claims_bases import ClaimBase
from tigrbl_identity_core import ClaimNameKind, ClaimType, ClaimValueType


class CwtSubjectClaim(ClaimBase):
    claim_name = 2
    default_name_kind = ClaimNameKind.INTEGER_LABEL
    default_registry = "IANA CWT Claims"
    default_claim_type = ClaimType.IDENTITY
    default_value_type = ClaimValueType.STRING
    default_standards = ("RFC8392",)

    @classmethod
    def validate_value(cls, value):
        if not (isinstance(value, str) and bool(value)):
            raise ValueError("CWT claim 2 has an invalid value")


__all__ = ["CwtSubjectClaim"]
