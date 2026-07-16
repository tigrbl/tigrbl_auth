from tigrbl_claim_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType


class TransactionIdClaim(ClaimBase):
    claim_name = "txn"
    default_claim_type = ClaimType.TRANSACTION
    default_value_type = ClaimValueType.STRING
    default_standards = ("OpenID Connect for Identity Assurance 1.0",)

    @classmethod
    def validate_value(cls, value):
        if not isinstance(value, str) or not value:
            raise ValueError("txn must be a non-empty string")


__all__ = ["TransactionIdClaim"]
