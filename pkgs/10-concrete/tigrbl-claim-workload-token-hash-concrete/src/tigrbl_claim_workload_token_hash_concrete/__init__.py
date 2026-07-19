import re

from tigrbl_claim_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType

_BASE64URL_DIGEST = re.compile(r"^[A-Za-z0-9_-]{43}$")

class WorkloadTokenHashClaim(ClaimBase):
    claim_name = "wth"
    default_claim_type = ClaimType.WORKLOAD
    default_value_type = ClaimValueType.STRING
    default_standards = ("draft-ietf-wimse-wpt-01",)

    @classmethod
    def validate_value(cls, value):
        if not isinstance(value, str) or not _BASE64URL_DIGEST.fullmatch(value):
            raise ValueError("wth must be a non-empty base64url SHA-256 digest")


__all__ = ["WorkloadTokenHashClaim"]