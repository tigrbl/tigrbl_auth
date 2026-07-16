from tigrbl_claim_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType


class AccessTokenHashClaim(ClaimBase):
    """OIDC ID Token hash of an access token (``at_hash``)."""

    claim_name = "at_hash"
    default_claim_type = ClaimType.AUTHENTICATION
    default_value_type = ClaimValueType.STRING
    default_standards = ("OpenID Connect Core 1.0",)

    @classmethod
    def validate_value(cls, value):
        if not isinstance(value, str) or not value:
            raise ValueError("at_hash must be a non-empty base64url digest")


__all__ = ["AccessTokenHashClaim"]
