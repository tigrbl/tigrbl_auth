from urllib.parse import urlparse
from tigrbl_claim_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType


class SecurityEventsClaim(ClaimBase):
    claim_name = "events"
    default_claim_type = ClaimType.SECURITY_EVENT
    default_value_type = ClaimValueType.JSON_OBJECT
    default_standards = ("RFC 8417",)

    @classmethod
    def validate_value(cls, value):
        if (
            not isinstance(value, dict)
            or not value
            or any(
                not isinstance(k, str)
                or not urlparse(k).scheme
                or not isinstance(v, dict)
                for k, v in value.items()
            )
        ):
            raise ValueError("events must map event-type URIs to objects")


__all__ = ["SecurityEventsClaim"]
