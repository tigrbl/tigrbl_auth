"""Standalone WIMSE other-token hashes claim."""

import re

from tigrbl_claim_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType

_BASE64URL_DIGEST = re.compile(r"^[A-Za-z0-9_-]{43}$")


class OtherTokenHashesClaim(ClaimBase):
    claim_name = "oth"
    default_claim_type = ClaimType.TRANSACTION
    default_value_type = ClaimValueType.JSON_OBJECT
    default_standards = ("draft-ietf-wimse-wpt-01",)

    @classmethod
    def validate_value(cls, value):
        if not isinstance(value, dict) or not value:
            raise ValueError("oth must be a non-empty token-name to digest object")
        for token_name, digest in value.items():
            if not isinstance(token_name, str) or not token_name.strip():
                raise ValueError("oth token names must be non-empty strings")
            if not isinstance(digest, str) or not _BASE64URL_DIGEST.fullmatch(digest):
                raise ValueError("oth values must be non-empty base64url SHA-256 digests")


__all__ = ["OtherTokenHashesClaim"]