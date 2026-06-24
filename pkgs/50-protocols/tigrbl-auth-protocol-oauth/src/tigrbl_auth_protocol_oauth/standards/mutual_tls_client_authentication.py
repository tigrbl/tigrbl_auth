"""Mutual-TLS client authentication and certificate-bound token helpers.

This module is intentionally dependency-light so Tier 3 evidence checkpoint evidence can execute
without the full runtime stack.  It covers three distinct concerns:

- certificate thumbprint extraction and confirmation-claim construction
- certificate-bound access-token verification on resource paths
- token-endpoint client authentication for tls_client_auth and
  self_signed_tls_client_auth registrations
"""

from __future__ import annotations

import base64
import hashlib
from typing import Any, Final, Mapping
from tigrbl_identity_core.standards import StandardOwner, describe_owner
from tigrbl_security_trust_contracts import MTLSClientAuthentication

from cryptography import x509
from cryptography.hazmat.primitives import serialization

from tigrbl_identity_runtime.settings import settings
from tigrbl_identity_core.errors import InvalidTokenError
from tigrbl_auth_protocol_oauth.standards._mtls_identity import (
    certificate_matches_registered_identity,
    certificate_san_values,
    certificate_subject_dn,
    normalize_presented_pem,
    registered_certificate_identity_metadata,
)

RFC8705_SPEC_URL: Final[str] = "https://www.rfc-editor.org/rfc/rfc8705"
TLS_CLIENT_AUTH_METHOD: Final[str] = "tls_client_auth"
SELF_SIGNED_TLS_CLIENT_AUTH_METHOD: Final[str] = "self_signed_tls_client_auth"
SUPPORTED_MTLS_AUTH_METHODS: Final[tuple[str, str]] = (
    TLS_CLIENT_AUTH_METHOD,
    SELF_SIGNED_TLS_CLIENT_AUTH_METHOD,
)

_CERTIFICATE_THUMBPRINT_HEADER_NAMES: Final[tuple[str, ...]] = (
    "X-Client-Cert-SHA256",
    "X-SSL-Client-SHA256",
    "X_SSL_CLIENT_CERT_SHA256",
    "MTLS-Client-Cert-SHA256",
)
_CERTIFICATE_PEM_HEADER_NAMES: Final[tuple[str, ...]] = (
    "X-Client-Cert",
    "X-SSL-Client-Cert",
    "MTLS-Client-Cert",
)
_SCOPE_CERTIFICATE_KEYS: Final[tuple[str, ...]] = (
    "client_cert_sha256",
    "tls_client_cert_sha256",
    "mtls_client_cert_sha256",
)
_SCOPE_CERTIFICATE_PEM_KEYS: Final[tuple[str, ...]] = (
    "client_cert_pem",
    "tls_client_cert_pem",
    "mtls_client_cert_pem",
)
_TRUSTED_CERTIFICATE_SCOPE_KEYS: Final[tuple[str, ...]] = (
    "client_cert_trusted",
    "tls_client_cert_trusted",
    "mtls_client_cert_trusted",
    "mtls_trusted_proxy",
)
_TLS_CERT_THUMBPRINT_KEYS: Final[tuple[str, ...]] = (
    "tls_client_certificate_thumbprint",
    "tls_client_certificate_thumbprints",
)
_SELF_SIGNED_CERT_THUMBPRINT_KEYS: Final[tuple[str, ...]] = (
    "self_signed_tls_client_certificate_thumbprint",
    "self_signed_tls_client_certificate_thumbprints",
)
_TLS_CLIENT_AUTH_IDENTITY_KEYS: Final[tuple[str, ...]] = (
    "tls_client_auth_subject_dn",
    "tls_client_auth_san_dns",
    "tls_client_auth_san_uri",
    "tls_client_auth_san_ip",
    "tls_client_auth_san_email",
)


OWNER = StandardOwner(
    label="RFC 8705",
    title="OAuth 2.0 Mutual-TLS Client Authentication and Certificate-Bound Access Tokens",
    runtime_status="mtls-runtime-integrated",
    public_surface=("/token", "/token/exchange", "/userinfo", "/introspect", "/revoke"),
    notes=(
        "mTLS client authentication, certificate-bound access-token validation, and "
        "runtime registration metadata checks are integrated with dependency-light helpers."
    ),
)


def thumbprint_from_cert_pem(cert_pem: bytes) -> str:
    cert = x509.load_pem_x509_certificate(cert_pem)
    der = cert.public_bytes(serialization.Encoding.DER)
    digest = hashlib.sha256(der).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def _normalize_presented_thumbprint(value: str | bytes | None) -> str | None:
    if value in {None, b"", ""}:
        return None
    if isinstance(value, bytes):
        if value.startswith(b"-----BEGIN CERTIFICATE-----"):
            return thumbprint_from_cert_pem(value)
        return value.decode("utf-8").strip() or None
    text = str(value).strip()
    if not text:
        return None
    if text.startswith("-----BEGIN CERTIFICATE-----"):
        return thumbprint_from_cert_pem(text.encode("utf-8"))
    return text


def certificate_confirmation_claim(thumbprint: str) -> dict[str, str]:
    return {"x5t#S256": str(thumbprint)}


def token_is_certificate_bound(payload: Mapping[str, Any]) -> bool:
    cnf = payload.get("cnf")
    return isinstance(cnf, Mapping) and bool(cnf.get("x5t#S256"))


is_certificate_bound_token = token_is_certificate_bound


def _headers_from_request(request_or_mapping: Any) -> Any:
    headers = getattr(request_or_mapping, "headers", None)
    if headers is None and isinstance(request_or_mapping, Mapping):
        headers = request_or_mapping
    return headers or {}


def _scope_from_request(request_or_mapping: Any) -> Mapping[str, Any]:
    scope = getattr(request_or_mapping, "scope", None)
    if scope is None and isinstance(request_or_mapping, Mapping):
        scope = request_or_mapping
    return scope if isinstance(scope, Mapping) else {}


def _scope_trusts_certificate_headers(request_or_mapping: Any) -> bool:
    scope = _scope_from_request(request_or_mapping)
    if any(bool(scope.get(key)) for key in _TRUSTED_CERTIFICATE_SCOPE_KEYS):
        return True
    state = getattr(request_or_mapping, "state", None)
    return any(bool(getattr(state, key, False)) for key in _TRUSTED_CERTIFICATE_SCOPE_KEYS)


def _header_certificate_thumbprint(request_or_mapping: Any) -> str | None:
    headers = _headers_from_request(request_or_mapping)
    if hasattr(headers, "get"):
        for name in _CERTIFICATE_THUMBPRINT_HEADER_NAMES:
            thumb = _normalize_presented_thumbprint(headers.get(name))
            if thumb:
                return thumb
        for name in _CERTIFICATE_PEM_HEADER_NAMES:
            thumb = _normalize_presented_thumbprint(headers.get(name))
            if thumb:
                return thumb
    return None


def _scope_certificate_thumbprint(request_or_mapping: Any) -> str | None:
    scope = _scope_from_request(request_or_mapping)
    for key in _SCOPE_CERTIFICATE_KEYS:
        thumb = _normalize_presented_thumbprint(scope.get(key))
        if thumb:
            return thumb
    for key in _SCOPE_CERTIFICATE_PEM_KEYS:
        thumb = _normalize_presented_thumbprint(scope.get(key))
        if thumb:
            return thumb
    return None


def presented_certificate_pem(request_or_mapping: Any, *, trusted_proxy: bool = False) -> bytes | None:
    scope = _scope_from_request(request_or_mapping)
    for key in _SCOPE_CERTIFICATE_PEM_KEYS:
        pem = normalize_presented_pem(scope.get(key))
        if pem:
            return pem
    if trusted_proxy or _scope_trusts_certificate_headers(request_or_mapping):
        headers = _headers_from_request(request_or_mapping)
        if hasattr(headers, "get"):
            for name in _CERTIFICATE_PEM_HEADER_NAMES:
                pem = normalize_presented_pem(headers.get(name))
                if pem:
                    return pem
    return None


def presented_trusted_certificate_thumbprint(request_or_mapping: Any, *, trusted_proxy: bool = False) -> str | None:
    scope_thumbprint = _scope_certificate_thumbprint(request_or_mapping)
    if scope_thumbprint:
        return scope_thumbprint
    if trusted_proxy or _scope_trusts_certificate_headers(request_or_mapping):
        return _header_certificate_thumbprint(request_or_mapping)
    return None


def presented_certificate_thumbprint(request_or_mapping: Any) -> str | None:
    return _header_certificate_thumbprint(request_or_mapping) or _scope_certificate_thumbprint(request_or_mapping)


def _coerce_thumbprints(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str) and not value.strip():
        return ()
    if isinstance(value, bytes) and not value.strip():
        return ()
    if isinstance(value, (list, tuple, set)) and not value:
        return ()
    if isinstance(value, (list, tuple, set)):
        result: list[str] = []
        for item in value:
            normalized = _normalize_presented_thumbprint(item)
            if normalized:
                result.append(normalized)
        return tuple(dict.fromkeys(result))
    normalized = _normalize_presented_thumbprint(value)
    return (normalized,) if normalized else ()


def registered_certificate_thumbprints(
    registration_metadata: Mapping[str, Any] | None,
    *,
    token_endpoint_auth_method: str | None = None,
) -> tuple[str, ...]:
    metadata = dict(registration_metadata or {})
    auth_method = str(token_endpoint_auth_method or metadata.get("token_endpoint_auth_method") or "").strip()
    thumbprints: list[str] = []
    if auth_method in {"", TLS_CLIENT_AUTH_METHOD}:
        for key in _TLS_CERT_THUMBPRINT_KEYS:
            thumbprints.extend(_coerce_thumbprints(metadata.get(key)))
    if auth_method in {"", SELF_SIGNED_TLS_CLIENT_AUTH_METHOD}:
        for key in _SELF_SIGNED_CERT_THUMBPRINT_KEYS:
            thumbprints.extend(_coerce_thumbprints(metadata.get(key)))
    return tuple(dict.fromkeys(thumbprints))


def authenticate_mtls_client(
    registration_metadata: Mapping[str, Any] | None,
    presented_thumbprint: str | bytes | None,
    *,
    presented_certificate_pem: str | bytes | None = None,
    token_endpoint_auth_method: str | None = None,
    enabled: bool | None = None,
) -> MTLSClientAuthentication:
    if enabled is None:
        enabled = settings.enable_rfc8705
    if not enabled:
        raise ValueError(f"RFC 8705 support disabled: {RFC8705_SPEC_URL}")
    auth_method = str(
        token_endpoint_auth_method
        or dict(registration_metadata or {}).get("token_endpoint_auth_method")
        or TLS_CLIENT_AUTH_METHOD
    ).strip()
    if auth_method not in SUPPORTED_MTLS_AUTH_METHODS:
        raise ValueError("unsupported token_endpoint_auth_method for mTLS client authentication")
    pem = normalize_presented_pem(presented_certificate_pem)
    effective_thumbprint = _normalize_presented_thumbprint(presented_thumbprint)
    if not effective_thumbprint and pem:
        effective_thumbprint = thumbprint_from_cert_pem(pem)
    if not effective_thumbprint:
        raise ValueError("client certificate thumbprint required for mTLS client authentication")
    allowed = registered_certificate_thumbprints(
        registration_metadata,
        token_endpoint_auth_method=auth_method,
    )
    if allowed:
        if effective_thumbprint not in set(allowed):
            raise ValueError("presented client certificate thumbprint is not registered for this client")
        return MTLSClientAuthentication(auth_method=auth_method, cert_thumbprint=effective_thumbprint)
    if auth_method == TLS_CLIENT_AUTH_METHOD and pem and certificate_matches_registered_identity(pem, registration_metadata):
        return MTLSClientAuthentication(auth_method=auth_method, cert_thumbprint=effective_thumbprint)
    if auth_method == TLS_CLIENT_AUTH_METHOD and any(registered_certificate_identity_metadata(registration_metadata).values()):
        raise ValueError("presented client certificate identity is not registered for this client")
    raise ValueError("registration metadata does not pin an allowed client certificate thumbprint")
    return MTLSClientAuthentication(auth_method=auth_method, cert_thumbprint=effective_thumbprint)


def validate_certificate_binding(
    payload: Mapping[str, Any],
    presented_thumbprint: str | bytes | None,
    *,
    enabled: bool | None = None,
) -> None:
    if enabled is None:
        enabled = settings.enable_rfc8705
    if not enabled:
        return
    cnf = payload.get("cnf")
    if not isinstance(cnf, Mapping):
        raise InvalidTokenError(f"cnf claim required by RFC 8705: {RFC8705_SPEC_URL}")
    bound = _normalize_presented_thumbprint(cnf.get("x5t#S256"))
    effective_thumbprint = _normalize_presented_thumbprint(presented_thumbprint)
    if not bound:
        raise InvalidTokenError(f"x5t#S256 confirmation claim required by RFC 8705: {RFC8705_SPEC_URL}")
    if bound != effective_thumbprint:
        raise InvalidTokenError(f"certificate thumbprint mismatch per RFC 8705: {RFC8705_SPEC_URL}")


def validate_request_certificate_binding(
    payload: Mapping[str, Any],
    request_or_mapping: Any,
    *,
    enabled: bool | None = None,
) -> str | None:
    thumbprint = presented_certificate_thumbprint(request_or_mapping)
    if token_is_certificate_bound(payload):
        validate_certificate_binding(payload, thumbprint, enabled=enabled)
    return thumbprint


def describe() -> dict[str, object]:
    return describe_owner(
        OWNER,
        spec_url=RFC8705_SPEC_URL,
        confirmation_claim="x5t#S256",
        supported_token_endpoint_auth_methods=list(SUPPORTED_MTLS_AUTH_METHODS),
        certificate_thumbprint_header_names=list(_CERTIFICATE_THUMBPRINT_HEADER_NAMES),
        certificate_pem_header_names=list(_CERTIFICATE_PEM_HEADER_NAMES),
        tls_client_auth_identity_metadata=list(_TLS_CLIENT_AUTH_IDENTITY_KEYS),
    )


__all__ = [
    "RFC8705_SPEC_URL",
    "TLS_CLIENT_AUTH_METHOD",
    "SELF_SIGNED_TLS_CLIENT_AUTH_METHOD",
    "SUPPORTED_MTLS_AUTH_METHODS",
    "MTLSClientAuthentication",
    "StandardOwner",
    "OWNER",
    "authenticate_mtls_client",
    "certificate_matches_registered_identity",
    "certificate_confirmation_claim",
    "certificate_san_values",
    "certificate_subject_dn",
    "describe",
    "is_certificate_bound_token",
    "presented_certificate_pem",
    "presented_certificate_thumbprint",
    "presented_trusted_certificate_thumbprint",
    "registered_certificate_identity_metadata",
    "registered_certificate_thumbprints",
    "thumbprint_from_cert_pem",
    "token_is_certificate_bound",
    "validate_certificate_binding",
    "validate_request_certificate_binding",
]
