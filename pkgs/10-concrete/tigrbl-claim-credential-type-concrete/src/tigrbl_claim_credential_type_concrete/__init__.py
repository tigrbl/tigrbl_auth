from tigrbl_claim_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType


class CredentialTypeClaim(ClaimBase):
    claim_name = "vct"
    default_claim_type = ClaimType.CREDENTIAL
    default_value_type = ClaimValueType.STRING
    default_standards = ("IETF SD-JWT VC",)

    @classmethod
    def validate_value(cls, value):
        if not isinstance(value, str) or not value:
            raise ValueError("vct must be a non-empty string")


__all__ = ["CredentialTypeClaim"]
