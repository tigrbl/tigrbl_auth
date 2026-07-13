from tigrbl_identity_claims_bases import ClaimBase
from tigrbl_identity_core import ClaimNameKind, ClaimType, ClaimValueType


class CwtIssuerClaim(ClaimBase):
    claim_name = 1
    default_name_kind = ClaimNameKind.INTEGER_LABEL
    default_registry = "IANA CWT Claims"
    default_claim_type = ClaimType.PROTOCOL
    default_value_type = ClaimValueType.STRING
    default_standards = ("RFC8392",)

    @classmethod
    def validate_value(cls, value):
        if not (isinstance(value, str) and bool(value)):
            raise ValueError("CWT claim 1 has an invalid value")


__all__ = ["CwtIssuerClaim"]
