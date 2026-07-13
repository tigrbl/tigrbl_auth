from tigrbl_identity_claims_bases import ClaimBase
from tigrbl_identity_core import ClaimNameKind, ClaimType, ClaimValueType


class CwtAudienceClaim(ClaimBase):
    claim_name = 3
    default_name_kind = ClaimNameKind.INTEGER_LABEL
    default_registry = "IANA CWT Claims"
    default_claim_type = ClaimType.PROTOCOL
    default_value_type = ClaimValueType.JSON_VALUE
    default_standards = ("RFC8392",)

    @classmethod
    def validate_value(cls, value):
        if not (isinstance(value, str) and bool(value) or isinstance(value, (list, tuple)) and bool(value) and all(isinstance(item, str) and item for item in value)):
            raise ValueError("CWT claim 3 has an invalid value")


__all__ = ["CwtAudienceClaim"]
