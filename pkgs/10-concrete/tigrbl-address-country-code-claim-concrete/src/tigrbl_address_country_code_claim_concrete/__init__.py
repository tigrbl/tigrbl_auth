from tigrbl_identity_claims_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType


class AddressCountryCodeClaim(ClaimBase):
    claim_name = "address.country_code"
    default_claim_type = ClaimType.IDENTITY
    default_value_type = ClaimValueType.STRING
    default_standards = ("OpenID Identity Assurance 1.0",)

    @classmethod
    def validate_value(cls, value):
        if (
            not isinstance(value, str)
            or len(value) != 2
            or not value.isalpha()
            or value != value.upper()
        ):
            raise ValueError(
                "address.country_code must be an uppercase ISO 3166-1 alpha-2 code"
            )


__all__ = ["AddressCountryCodeClaim"]
