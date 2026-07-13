from urllib.parse import urlsplit

from tigrbl_identity_claims_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType


class HttpUriClaim(ClaimBase):
    claim_name = "htu"
    default_claim_type = ClaimType.AUTHENTICATION
    default_value_type = ClaimValueType.URI
    default_standards = ("RFC9449",)

    @classmethod
    def validate_value(cls, value):
        parsed = urlsplit(value) if isinstance(value, str) else None
        if parsed is None or not parsed.scheme or not parsed.netloc or parsed.fragment:
            raise ValueError("htu must be an absolute URI without a fragment")


__all__ = ["HttpUriClaim"]
