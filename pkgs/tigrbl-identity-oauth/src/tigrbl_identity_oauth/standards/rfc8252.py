"""Compatibility facade for canonical RFC 8252 native-app helpers."""

from tigrbl_auth.standards.oauth2.native_apps import (
    RFC8252_SPEC_URL,
    NativeRedirectAssessment,
    classify_native_redirect_uri,
    is_native_redirect_uri,
    validate_native_authorization_request,
    validate_native_client_metadata,
    validate_native_redirect_uri,
    validate_native_token_request,
)

__all__ = [
    "RFC8252_SPEC_URL",
    "NativeRedirectAssessment",
    "classify_native_redirect_uri",
    "is_native_redirect_uri",
    "validate_native_authorization_request",
    "validate_native_client_metadata",
    "validate_native_redirect_uri",
    "validate_native_token_request",
]
