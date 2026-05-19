"""Compatibility facade for canonical RFC 8705 mTLS helpers."""

from tigrbl_auth.standards.oauth2.mtls import (
    RFC8705_SPEC_URL,
    SELF_SIGNED_TLS_CLIENT_AUTH_METHOD,
    SUPPORTED_MTLS_AUTH_METHODS,
    TLS_CLIENT_AUTH_METHOD,
    authenticate_mtls_client,
    certificate_confirmation_claim,
    presented_certificate_thumbprint,
    registered_certificate_thumbprints,
    thumbprint_from_cert_pem,
    token_is_certificate_bound,
    validate_certificate_binding,
    validate_request_certificate_binding,
)

__all__ = [
    "RFC8705_SPEC_URL",
    "TLS_CLIENT_AUTH_METHOD",
    "SELF_SIGNED_TLS_CLIENT_AUTH_METHOD",
    "SUPPORTED_MTLS_AUTH_METHODS",
    "authenticate_mtls_client",
    "certificate_confirmation_claim",
    "presented_certificate_thumbprint",
    "registered_certificate_thumbprints",
    "thumbprint_from_cert_pem",
    "token_is_certificate_bound",
    "validate_certificate_binding",
    "validate_request_certificate_binding",
]
