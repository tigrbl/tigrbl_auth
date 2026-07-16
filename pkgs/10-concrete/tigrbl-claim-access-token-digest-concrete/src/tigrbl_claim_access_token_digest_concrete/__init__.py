"""Standalone RFC 9449 access-token digest claim."""

from tigrbl_claim_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType


class AccessTokenDigestClaim(ClaimBase):
    claim_name = "ath"
    default_claim_type = ClaimType.AUTHENTICATION
    default_value_type = ClaimValueType.STRING
    default_standards = ("RFC9449",)

    @classmethod
    def validate_value(cls, value):
        if not isinstance(value, str) or not value:
            raise ValueError("ath must be a non-empty base64url digest")


__all__ = ["AccessTokenDigestClaim"]
