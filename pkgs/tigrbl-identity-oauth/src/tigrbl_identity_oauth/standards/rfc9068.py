"""Compatibility facade for canonical RFC 9068 JWT access-token helpers."""

from tigrbl_auth.standards.oauth2.jwt_access_tokens import (
    RFC9068_SPEC_URL,
    add_jwt_access_token_claims,
    validate_jwt_access_token_claims,
)

add_rfc9068_claims = add_jwt_access_token_claims
validate_rfc9068_claims = validate_jwt_access_token_claims

__all__ = [
    "RFC9068_SPEC_URL",
    "add_jwt_access_token_claims",
    "validate_jwt_access_token_claims",
    "add_rfc9068_claims",
    "validate_rfc9068_claims",
]
