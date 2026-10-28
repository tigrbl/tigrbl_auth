from tba_bases_claim import ClaimBase
from tba_primitives_identity import ClaimType, ClaimValueType


class EatProfileClaim(ClaimBase):
    claim_name = "eat_profile"
    default_claim_type = ClaimType.ATTESTATION
    default_value_type = ClaimValueType.JSON_VALUE
    default_standards = ("RFC 9711",)

    @classmethod
    def validate_value(cls, value):
        if not isinstance(value, (str, int)) or isinstance(value, bool):
            raise ValueError("eat_profile must be a URI/OID string or integer label")


__all__ = ["EatProfileClaim"]
