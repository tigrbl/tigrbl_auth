from tigrbl_claim_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType


class ConfirmationClaim(ClaimBase):
    claim_name = "cnf"
    default_claim_type = ClaimType.AUTHORIZATION
    default_value_type = ClaimValueType.JSON_OBJECT
    default_standards = ("RFC 7800", "RFC 8705", "RFC 9449")

    @classmethod
    def validate_value(cls, value):
        if (
            not isinstance(value, dict)
            or len(value) != 1
            or not ({"jkt", "x5t#S256"} & set(value))
        ):
            raise ValueError("cnf requires exactly one supported confirmation member")


__all__ = ["ConfirmationClaim"]
