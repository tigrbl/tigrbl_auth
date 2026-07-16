from datetime import date
from urllib.parse import urlsplit

from tigrbl_claim_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType


def _absolute_uri(value):
    parsed = urlsplit(value) if isinstance(value, str) else None
    return parsed is not None and bool(parsed.scheme and parsed.netloc)


def _birthdate(value):
    if not isinstance(value, str) or not value:
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return value.startswith("0000-") and len(value) == 10
    return True


class AuthorizationCodeHashClaim(ClaimBase):
    claim_name = "c_hash"
    default_claim_type = ClaimType.AUTHENTICATION
    default_value_type = ClaimValueType.STRING
    default_standards = ("OIDC Core 1.0",)

    @classmethod
    def validate_value(cls, value):
        if not (isinstance(value, str) and bool(value)):
            raise ValueError("c_hash has an invalid OIDC claim value")


__all__ = ["AuthorizationCodeHashClaim"]
