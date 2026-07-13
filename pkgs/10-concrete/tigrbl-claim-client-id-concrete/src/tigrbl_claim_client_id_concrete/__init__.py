from tigrbl_identity_claims_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType


class ClientIdClaim(ClaimBase):
    claim_name = "client_id"
    default_claim_type = ClaimType.AUTHORIZATION
    default_value_type = ClaimValueType.STRING
    default_standards = ("RFC 9068",)

    @classmethod
    def validate_value(cls, value):
        if not isinstance(value, str) or not value:
            raise ValueError("client_id must be a non-empty string")


__all__ = ["ClientIdClaim"]
