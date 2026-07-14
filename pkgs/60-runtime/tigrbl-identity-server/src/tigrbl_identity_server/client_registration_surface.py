"""Runtime security, policy, and composition for RFC 7591 and RFC 7592."""

from __future__ import annotations

import secrets
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from uuid import UUID, uuid4

from tigrbl import Request, TigrblApp
from tigrbl.runtime.status import HTTPException, status
from tigrbl_auth_api_oauth_registration import (
    build_client_registration_router,
    include_client_registration_endpoint as include_http_registration_endpoint,
)
from tigrbl_auth_protocol_oauth.schemas import (
    DynamicClientRegistrationIn,
    DynamicClientRegistrationManagementIn,
    DynamicClientRegistrationOut,
)
from tigrbl_auth_protocol_oauth.standards.client_registration_management import (
    RFC7592ClientRegistrationManagementService,
)
from tigrbl_auth_protocol_oauth.standards.dynamic_client_registration import (
    RFC7591DynamicClientRegistrationService,
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
from tigrbl_auth_protocol_oauth.standards.oauth_security_bcp import (
    runtime_security_profile,
)
from tigrbl_identity_contracts.oauth import (
    ClientRegistrationCreateRequest,
    ClientRegistrationRecord,
    ClientRegistrationUpdateRequest,
)
from tigrbl_identity_core.constant_time import text_equal
from tigrbl_identity_core.digests import token_hash
from tigrbl_identity_jose.key_management import hash_pw
from tigrbl_identity_runtime.deployment import (
    deployment_from_app,
    deployment_from_request,
    resolve_deployment,
)
from tigrbl_identity_runtime.settings import settings
from tigrbl_identity_storage.tables.tenant import Tenant
from tigrbl_identity_storage_runtime.engine import get_db
from tigrbl_identity_storage_runtime.ops.common import (
    create_record,
    first_record,
    read_record,
)
from tigrbl_identity_storage_runtime.tenant_state import enabled_tenant_record

from .security.client_registration import build_client_registration_capability


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


def _tenant_from_operator_record(
    record: dict[str, object], *, tenant_slug: str
) -> Tenant | None:
    data = record.get("data") if isinstance(record.get("data"), dict) else {}
    sql_tenant_id = record.get("sql_tenant_id") or data.get("sql_tenant_id")
    if not sql_tenant_id:
        return None
    try:
        tenant_id = UUID(str(sql_tenant_id))
    except ValueError:
        return None
    base_name = (
        str(record.get("name") or data.get("name") or "Tenant").strip()
        or "Tenant"
    )
    return Tenant(
        id=tenant_id,
        slug=tenant_slug,
        name=f"{base_name}-{tenant_slug}"[:120],
        email=f"{tenant_slug}@tenant.local"[:120],
    )


async def _resolve_registration_tenant(*, db, tenant_slug: str) -> Tenant:
    tenant = await first_record(Tenant, db, {"slug": tenant_slug})
    if tenant is not None:
        return tenant
    record = enabled_tenant_record(Path.cwd(), tenant_slug)
    if record is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "tenant not found")
    tenant = _tenant_from_operator_record(record, tenant_slug=tenant_slug)
    if tenant is not None:
        payload = {
            "id": tenant.id,
            "slug": tenant.slug,
            "name": tenant.name,
            "email": tenant.email,
        }
    else:
        base_name = str(record.get("name") or "Tenant").strip() or "Tenant"
        payload = {
            "slug": tenant_slug,
            "name": f"{base_name}-{tenant_slug}"[:120],
            "email": f"{tenant_slug}@tenant.local"[:120],
        }
    try:
        return await create_record(Tenant, db, payload)
    except Exception as exc:
        tenant = await first_record(Tenant, db, {"slug": tenant_slug})
        if tenant is None:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                "tenant materialization conflict",
            ) from exc
        return tenant


def _require_https_uri(uri: str, *, field: str) -> None:
    if urlparse(uri).scheme != "https":
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"{field} must use https")


def _bearer_token(request: Request) -> str | None:
    headers = getattr(request, "headers", {}) or {}
    authz = headers.get("Authorization") or headers.get("authorization")
    if not authz:
        return None
    prefix, _, token = str(authz).partition(" ")
    if prefix.lower() != "bearer" or not token:
        return None
    return token.strip() or None


def _validated_token_endpoint_auth_method(
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


def _merge_registration_metadata(
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


async def _validated_registration_payload(
    *,
    db,
    payload: DynamicClientRegistrationIn,
    deployment=None,
) -> tuple[Tenant, dict[str, object]]:
    deployment = deployment if deployment is not None else resolve_deployment(settings)
    policy = runtime_security_profile(deployment)
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
    tenant = await _resolve_registration_tenant(
        db=db,
        tenant_slug=payload.tenant_slug,
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
    _validated_token_endpoint_auth_method(payload, policy=policy)
    for uri in payload.post_logout_redirect_uris or []:
        _require_https_uri(uri, field="post_logout_redirect_uris")
    if payload.frontchannel_logout_uri:
        _require_https_uri(
            payload.frontchannel_logout_uri,
            field="frontchannel_logout_uri",
        )
    if payload.backchannel_logout_uri:
        _require_https_uri(
            payload.backchannel_logout_uri,
            field="backchannel_logout_uri",
        )
    return tenant, derived_metadata


def _registration_response(
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
        client_id_issued_at=int(
            (issued_at or datetime.now(timezone.utc)).timestamp()
        ),
        client_secret_expires_at=0,
        redirect_uris=list(record.redirect_uris),
        grant_types=list(record.grant_types),
        response_types=list(record.response_types),
        token_endpoint_auth_method=metadata.get(
            "token_endpoint_auth_method", "client_secret_basic"
        ),
        token_endpoint_auth_signing_alg=metadata.get(
            "token_endpoint_auth_signing_alg"
        ),
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


def _deployment(request: Request):
    if getattr(request, "app", None) is not None:
        return deployment_from_request(request, settings)
    return resolve_deployment(settings)


def _rfc7591_service(request: Request, db):
    deployment = _deployment(request)
    return RFC7591DynamicClientRegistrationService(
        build_client_registration_capability(db),
        enabled=deployment.flag_enabled("enable_rfc7591"),
    )


def _rfc7592_service(request: Request, db):
    deployment = _deployment(request)
    return RFC7592ClientRegistrationManagementService(
        build_client_registration_capability(db),
        enabled=deployment.flag_enabled("enable_rfc7592"),
    )


async def register_client(
    request: Request,
    db,
    payload: DynamicClientRegistrationIn,
) -> dict[str, object]:
    deployment = _deployment(request)
    if not deployment.flag_enabled("enable_rfc7591"):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "dynamic client registration disabled",
        )
    tenant, derived_metadata = await _validated_registration_payload(
        db=db,
        payload=payload,
        deployment=deployment,
    )
    policy = runtime_security_profile(deployment)
    client_id = str(uuid4())
    client_secret = secrets.token_urlsafe(32)
    registration_access_token = None
    registration_access_token_hash = None
    registration_client_uri = None
    if deployment.flag_enabled("enable_rfc7592"):
        registration_access_token = secrets.token_urlsafe(32)
        registration_access_token_hash = token_hash(registration_access_token)
        registration_client_uri = (
            f"{str(deployment.issuer or settings.issuer).rstrip('/')}"
            f"/register/{client_id}"
        )
    metadata = _merge_registration_metadata(
        payload,
        derived_metadata=derived_metadata,
    )
    record = await _rfc7591_service(request, db).register(
        ClientRegistrationCreateRequest(
            client_id=client_id,
            tenant_id=str(tenant.id),
            client_secret_hash=hash_pw(client_secret),
            redirect_uris=tuple(payload.redirect_uris),
            grant_types=tuple(payload.grant_types),
            response_types=tuple(payload.response_types),
            metadata=metadata,
            contacts=tuple(str(item) for item in payload.contacts or ()),
            software_id=payload.software_id,
            software_version=payload.software_version,
            registration_access_token_hash=registration_access_token_hash,
            registration_client_uri=registration_client_uri,
        )
    )
    suppress_secret = policy.fapi_mode and (
        payload.token_endpoint_auth_method in set(policy.allowed_client_auth_methods)
    )
    return _registration_response(
        record,
        registration_access_token=registration_access_token,
        client_secret=None if suppress_secret else client_secret,
    )


async def _require_registration_access(
    request: Request,
    db,
    client_id: str,
) -> tuple[ClientRegistrationRecord, str]:
    try:
        normalized_client_id = str(UUID(str(client_id)))
    except ValueError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "invalid client_id") from exc
    service = _rfc7592_service(request, db)
    if not service.enabled:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "dynamic client registration management disabled",
        )
    record = await service.get(normalized_client_id)
    if record is None or record.disabled_at is not None or not record.client_active:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "client registration not found",
        )
    bearer = _bearer_token(request)
    if not bearer:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            {
                "error": "invalid_token",
                "error_description": "registration access token required",
            },
        )
    presented_hash = token_hash(bearer)
    if not record.registration_access_token_hash or not text_equal(
        presented_hash,
        record.registration_access_token_hash,
    ):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            {
                "error": "invalid_token",
                "error_description": "invalid registration access token",
            },
        )
    return record, bearer


async def get_registered_client(
    request: Request,
    db,
    client_id: str,
) -> dict[str, object]:
    record, bearer = await _require_registration_access(request, db, client_id)
    return _registration_response(record, registration_access_token=bearer)


async def update_registered_client(
    request: Request,
    db,
    client_id: str,
    payload: DynamicClientRegistrationManagementIn,
) -> dict[str, object]:
    record, bearer = await _require_registration_access(request, db, client_id)
    current = dict(record.metadata)
    tenant = await read_record(Tenant, db, record.tenant_id)
    current.setdefault("tenant_slug", tenant.slug if tenant is not None else "public")
    current.setdefault("redirect_uris", list(record.redirect_uris))
    current.setdefault("grant_types", list(record.grant_types))
    current.setdefault("response_types", list(record.response_types))
    current.setdefault("token_endpoint_auth_method", "client_secret_basic")
    incoming = payload.model_dump(exclude_none=True)
    current.update(incoming)
    validated = DynamicClientRegistrationIn(**current)
    _, derived_metadata = await _validated_registration_payload(
        db=db,
        payload=validated,
        deployment=_deployment(request),
    )
    metadata = _merge_registration_metadata(
        validated,
        derived_metadata=derived_metadata,
    )
    changed = await _rfc7592_service(request, db).update(
        ClientRegistrationUpdateRequest(
            client_id=record.client_id,
            redirect_uris=tuple(validated.redirect_uris),
            grant_types=tuple(validated.grant_types),
            response_types=tuple(validated.response_types),
            metadata=metadata,
            contacts=tuple(str(item) for item in validated.contacts or ()),
            software_id=validated.software_id,
            software_version=validated.software_version,
            updated_fields=tuple(sorted(incoming)),
        )
    )
    return _registration_response(changed, registration_access_token=bearer)


async def delete_registered_client(
    request: Request,
    db,
    client_id: str,
) -> dict[str, object]:
    record, _ = await _require_registration_access(request, db, client_id)
    disabled = await _rfc7592_service(request, db).delete(record.client_id)
    return {"status": "deleted", "client_id": disabled.client_id}


router = build_client_registration_router(
    register_client=register_client,
    get_registration=get_registered_client,
    update_registration=update_registered_client,
    delete_registration=delete_registered_client,
    get_db=get_db,
)


def include_client_registration_endpoint(app: TigrblApp) -> None:
    deployment = deployment_from_app(app, settings)
    include_http_registration_endpoint(
        app,
        router,
        registration_enabled=deployment.flag_enabled("enable_rfc7591"),
        management_enabled=deployment.flag_enabled("enable_rfc7592"),
    )


include_rfc7591 = include_client_registration_endpoint
include_rfc7592 = include_client_registration_endpoint


__all__ = [
    "_bearer_token",
    "_merge_registration_metadata",
    "_registration_response",
    "_require_registration_access",
    "_validated_registration_payload",
    "_validated_token_endpoint_auth_method",
    "delete_registered_client",
    "get_registered_client",
    "include_client_registration_endpoint",
    "include_rfc7591",
    "include_rfc7592",
    "register_client",
    "router",
    "update_registered_client",
]
