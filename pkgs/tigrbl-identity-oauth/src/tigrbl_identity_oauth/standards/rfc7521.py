"""Compatibility facade for canonical RFC 7521 assertion helpers."""

from tigrbl_auth.standards.oauth2.assertion_framework import (
    JWT_BEARER_ASSERTION_TYPE,
    JWT_BEARER_GRANT_TYPE,
    OWNER,
    OPTIONAL_FRESHNESS_CLAIMS,
    RFC7521_SPEC_URL,
    REQUIRED_CLAIMS,
    STATUS,
    StandardOwner,
    build_assertion_contract_examples,
    describe,
    validate_assertion_grant_request,
    validate_jwt_assertion,
    validate_temporal_claims,
)

__all__ = [
    "STATUS",
    "RFC7521_SPEC_URL",
    "JWT_BEARER_GRANT_TYPE",
    "JWT_BEARER_ASSERTION_TYPE",
    "REQUIRED_CLAIMS",
    "OPTIONAL_FRESHNESS_CLAIMS",
    "StandardOwner",
    "OWNER",
    "build_assertion_contract_examples",
    "validate_assertion_grant_request",
    "validate_jwt_assertion",
    "validate_temporal_claims",
    "describe",
]
