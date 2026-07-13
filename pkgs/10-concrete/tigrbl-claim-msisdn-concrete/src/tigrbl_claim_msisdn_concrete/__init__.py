from tigrbl_identity_claims_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType


class MsisdnClaim(ClaimBase):
    claim_name = "msisdn"
    default_claim_type = ClaimType.IDENTITY
    default_value_type = ClaimValueType.STRING
    default_standards = ("OpenID Identity Assurance 1.0",)

    @classmethod
    def validate_value(cls, value):
        if (
            not isinstance(value, str)
            or not value.startswith("+")
            or not value[1:].isdigit()
        ):
            raise ValueError("msisdn must be an E.164-style number")


__all__ = ["MsisdnClaim"]
