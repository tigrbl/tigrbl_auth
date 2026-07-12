"""Compatibility exports for standalone identity assurance."""

from tigrbl_identity_assurance_concrete import (
    CLAIMS_SPEC_URL,
    OIDC_SPEC_URL,
    SCHEMA_SPEC_URL,
    parse_verified_claims,
    serialize_verified_claims,
)

__all__ = [
    "CLAIMS_SPEC_URL",
    "OIDC_SPEC_URL",
    "SCHEMA_SPEC_URL",
    "parse_verified_claims",
    "serialize_verified_claims",
]
