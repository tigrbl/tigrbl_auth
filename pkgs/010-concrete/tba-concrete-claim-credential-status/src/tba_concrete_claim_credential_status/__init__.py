from tba_bases_claim import ClaimBase
from tba_primitives_identity import ClaimType, ClaimValueType


class CredentialStatusClaim(ClaimBase):
    claim_name = "status"
    default_claim_type = ClaimType.CREDENTIAL
    default_value_type = ClaimValueType.JSON_OBJECT
    default_standards = ("IETF SD-JWT VC",)

    @classmethod
    def validate_value(cls, value):
        if not isinstance(value, dict) or not value:
            raise ValueError("status must be a non-empty object")


__all__ = ["CredentialStatusClaim"]
