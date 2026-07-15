"""Payload validation and response mapping for dynamic client registration."""

from __future__ import annotations

from datetime import datetime, timezone
from urllib.parse import urlparse

from tigrbl import Request
from tigrbl.runtime.status import HTTPException, status
from tigrbl_auth_protocol_oauth.schemas import (
    DynamicClientRegistrationIn,
    DynamicClientRegistrationOut,
)
from tigrbl_auth_protocol_oauth.standards.jwt_client_auth import (
    PRIVATE_KEY_JWT_AUTH_METHOD,
    SUPPORTED_CLIENT_ASSERTION_SIGNING_ALGS,
)
from tigrbl_auth_protocol_oauth.standards.mutual_tls_client_authentication import (
    SELF_SIGNED_TLS_CLIENT_AUTH_METHOD,
    SUPPORTED_MTLS_AUTH_METHODS,
    TLS_CLIENT_AUTH_METHOD,
)
from tigrbl_auth_protocol_oauth.standards.native_apps import (
    is_native_redirect_uri,
    validate_native_client_metadata,
    validate_native_redirect_uri,
)
from tigrbl_identity_contracts.oauth import ClientRegistrationRecord


DEFAULT_TOKEN_ENDPOINT_AUTH_METHODS = {
    "client_secret_basic",
    "client_secret_post",
    PRIVATE_KEY_JWT_AUTH_METHOD,
    *SUPPORTED_MTLS_AUTH_METHODS,
}
TLS_CLIENT_AUTH_IDENTITY_FIELDS = (
    "tls_client_auth_subject_dn",
    "tls_client_auth_san_dns",
    "tls_client_auth_san_uri",
    "tls_client_auth_san_ip",
    "tls_client_auth_san_email",
)


def bearer_token(request: Request) -> str | None:
    headers = getattr(request, "headers", {}) or {}
    authz = headers.get("Authorization") or headers.get("authorization")
    if not authz:
        return None
    prefix, _, token = str(authz).partition(" ")
    if prefix.lower() != "bearer" or not token:
        return None
    return token.strip() or None


def validate_token_endpoint_auth_method(
    payload: DynamicClientRegistrationIn, *, policy
) -> None:
    method = str(payload.token_endpoint_auth_method or "client_secret_basic")
    if method not in DEFAULT_TOKEN_ENDPOINT_AUTH_METHODS:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"invalid_client_metadata: unsupported token_endpoint_auth_method {method!r}",
        )
    if policy.fapi_mode and method not in set(policy.allowed_client_auth_methods):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "invalid_client_metadata: FAPI clients must use private_key_jwt, "
            "tls_client_auth, or self_signed_tls_client_auth",
        )
    if method == PRIVATE_KEY_JWT_AUTH_METHOD:
        if not payload.jwks_uri:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "invalid_client_metadata: private_key_jwt requires jwks_uri",
            )
        if (
            payload.token_endpoint_auth_signing_alg
            and payload.token_endpoint_auth_signing_alg
            not in SUPPORTED_CLIENT_ASSERTION_SIGNING_ALGS
        ):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "invalid_client_metadata: unsupported "
                f"token_endpoint_auth_signing_alg {payload.token_endpoint_auth_signing_alg!r}",
            )
    elif method == TLS_CLIENT_AUTH_METHOD:
        has_identity_metadata = any(
            getattr(payload, field, None) for field in TLS_CLIENT_AUTH_IDENTITY_FIELDS
        )
        if not payload.tls_client_certificate_thumbprint and not has_identity_metadata:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "invalid_client_metadata: tls_client_auth requires "
                "tls_client_certificate_thumbprint, subject_dn, or SAN metadata",
            )
    elif (
        method == SELF_SIGNED_TLS_CLIENT_AUTH_METHOD
        and not payload.self_signed_tls_client_certificate_thumbprint
    ):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "invalid_client_metadata: self_signed_tls_client_auth requires "
            "self_signed_tls_client_certificate_thumbprint",
        )


def merge_registration_metadata(
    payload: DynamicClientRegistrationIn, *, derived_metadata: dict[str, object]
) -> dict[str, object]:
    metadata = payload.model_dump()
    metadata.update(derived_metadata)
    metadata.setdefault(
        "application_type",
        "native" if derived_metadata.get("native_application") else "web",
    )
    if payload.token_endpoint_auth_method == PRIVATE_KEY_JWT_AUTH_METHOD:
        metadata.setdefault(
            "token_endpoint_auth_signing_alg",
            SUPPORTED_CLIENT_ASSERTION_SIGNING_ALGS[0],
        )
    return metadata


def validate_registration_metadata(
    payload: DynamicClientRegistrationIn, *, policy
) -> dict[str, object]:
    unsupported_grants = sorted(
        set(payload.grant_types) - set(policy.allowed_grant_types)
    )
    if unsupported_grants:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"invalid_client_metadata: unsupported grant_types {unsupported_grants}",
        )
    unsupported_responses = sorted(
        set(payload.response_types) - set(policy.allowed_response_types)
    )
    if unsupported_responses:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "invalid_client_metadata: unsupported response_types "
            f"{unsupported_responses}",
        )
    redirect_uris = list(payload.redirect_uris or [])
    if not redirect_uris:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "redirect_uris required")
    for uri in redirect_uris:
        if is_native_redirect_uri(uri):
            validate_native_redirect_uri(uri)
        elif urlparse(uri).scheme != "https":
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "redirect_uris must use https",
            )
    try:
        derived_metadata = validate_native_client_metadata(
            redirect_uris=redirect_uris,
            response_types=payload.response_types,
            grant_types=payload.grant_types,
        )
    except ValueError as exc:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"invalid_client_metadata: {exc}",
        ) from exc
    validate_token_endpoint_auth_method(payload, policy=policy)
    for uri in payload.post_logout_redirect_uris or []:
        _require_https_uri(uri, field="post_logout_redirect_uris")
    if payload.frontchannel_logout_uri:
        _require_https_uri(
            payload.frontchannel_logout_uri, field="frontchannel_logout_uri"
        )
    if payload.backchannel_logout_uri:
        _require_https_uri(
            payload.backchannel_logout_uri, field="backchannel_logout_uri"
        )
    return derived_metadata


def registration_response(
    record: ClientRegistrationRecord,
    *,
    registration_access_token: str | None = None,
    client_secret: str | None = None,
) -> dict[str, object]:
    metadata = dict(record.metadata)
    issued_at = record.issued_at
    if issued_at is not None and issued_at.tzinfo is None:
        issued_at = issued_at.replace(tzinfo=timezone.utc)
    return DynamicClientRegistrationOut(
        client_id=record.client_id,
        client_secret=client_secret,
        client_id_issued_at=int((issued_at or datetime.now(timezone.utc)).timestamp()),
        client_secret_expires_at=0,
        redirect_uris=list(record.redirect_uris),
        grant_types=list(record.grant_types),
        response_types=list(record.response_types),
        token_endpoint_auth_method=metadata.get(
            "token_endpoint_auth_method", "client_secret_basic"
        ),
        token_endpoint_auth_signing_alg=metadata.get("token_endpoint_auth_signing_alg"),
        tls_client_certificate_thumbprint=metadata.get(
            "tls_client_certificate_thumbprint"
        ),
        self_signed_tls_client_certificate_thumbprint=metadata.get(
            "self_signed_tls_client_certificate_thumbprint"
        ),
        tls_client_auth_subject_dn=metadata.get("tls_client_auth_subject_dn"),
        tls_client_auth_san_dns=metadata.get("tls_client_auth_san_dns"),
        tls_client_auth_san_uri=metadata.get("tls_client_auth_san_uri"),
        tls_client_auth_san_ip=metadata.get("tls_client_auth_san_ip"),
        tls_client_auth_san_email=metadata.get("tls_client_auth_san_email"),
        application_type=metadata.get("application_type"),
        scope=metadata.get("scope"),
        client_name=metadata.get("client_name"),
        client_uri=metadata.get("client_uri"),
        jwks_uri=metadata.get("jwks_uri"),
        contacts=list(record.contacts) or None,
        software_id=record.software_id,
        software_version=record.software_version,
        post_logout_redirect_uris=metadata.get("post_logout_redirect_uris"),
        frontchannel_logout_uri=metadata.get("frontchannel_logout_uri"),
        frontchannel_logout_session_required=metadata.get(
            "frontchannel_logout_session_required", True
        ),
        backchannel_logout_uri=metadata.get("backchannel_logout_uri"),
        backchannel_logout_session_required=metadata.get(
            "backchannel_logout_session_required", True
        ),
        registration_access_token=registration_access_token,
        registration_client_uri=record.registration_client_uri,
    ).model_dump(exclude_none=True)


def _require_https_uri(uri: str, *, field: str) -> None:
    if urlparse(uri).scheme != "https":
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"{field} must use https")
