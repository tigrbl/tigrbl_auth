from __future__ import annotations

import secrets
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from uuid import UUID, uuid4

from tigrbl_identity_contracts.rest import (
    DynamicClientRegistrationIn,
    DynamicClientRegistrationManagementIn,
    DynamicClientRegistrationOut,
)
from tigrbl_identity_runtime.deployment import deployment_from_request, resolve_deployment
from tigrbl_identity_runtime.settings import settings
from tigrbl_identity_server.framework import HTTPException, status
from tigrbl_identity_server.security.handler_records import (
    append_audit_event_record,
    create_handler_record,
    first_handler_record,
    read_handler_record,
    token_hash,
    update_handler_record,
)
from tigrbl_identity_principals.tenant_discovery import enabled_tenant_record
from tigrbl_auth_protocol_oauth.standards.jwt_client_auth import (
    PRIVATE_KEY_JWT_AUTH_METHOD,
    SUPPORTED_CLIENT_ASSERTION_SIGNING_ALGS,
)
from tigrbl_auth_protocol_oauth.standards.mtls import (
    SELF_SIGNED_TLS_CLIENT_AUTH_METHOD,
    SUPPORTED_MTLS_AUTH_METHODS,
    TLS_CLIENT_AUTH_METHOD,
)
from tigrbl_auth_protocol_oauth.standards.native_apps import (
    is_native_redirect_uri,
    validate_native_client_metadata,
    validate_native_redirect_uri,
)
from tigrbl_auth_protocol_oauth.standards.rfc9700 import runtime_security_profile
from tigrbl_identity_storage.tables import Client, ClientRegistration, Tenant


DEFAULT_TOKEN_ENDPOINT_AUTH_METHODS = {"client_secret_basic", "client_secret_post", PRIVATE_KEY_JWT_AUTH_METHOD, *SUPPORTED_MTLS_AUTH_METHODS}


def _tenant_from_operator_record(record: dict[str, object], *, tenant_slug: str) -> Tenant | None:
    data = record.get("data") if isinstance(record.get("data"), dict) else {}
    sql_tenant_id = record.get("sql_tenant_id") or data.get("sql_tenant_id")
    if not sql_tenant_id:
        return None
    try:
        tenant_id = UUID(str(sql_tenant_id))
    except ValueError:
        return None
    base_name = str(record.get("name") or data.get("name") or "Tenant").strip() or "Tenant"
    return Tenant(
        id=tenant_id,
        slug=tenant_slug,
        name=f"{base_name}-{tenant_slug}"[:120],
        email=f"{tenant_slug}@tenant.local"[:120],
    )


async def _resolve_registration_tenant(*, db, tenant_slug: str) -> Tenant:
    tenant = await first_handler_record(Tenant, db, {"slug": tenant_slug})
    if tenant is not None:
        return tenant

    record = enabled_tenant_record(Path.cwd(), tenant_slug)
    if record is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'tenant not found')
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
        name = f"{base_name}-{tenant_slug}"[:120]
        email = f"{tenant_slug}@tenant.local"[:120]
        payload = {"slug": tenant_slug, "name": name, "email": email}

    try:
        tenant = await create_handler_record(Tenant, db, payload)
    except Exception as exc:
        tenant = await first_handler_record(Tenant, db, {"slug": tenant_slug})
        if tenant is None:
            raise HTTPException(status.HTTP_409_CONFLICT, 'tenant materialization conflict') from exc
    return tenant



def _require_https_uri(uri: str, *, field: str) -> None:
    parsed = urlparse(uri)
    if parsed.scheme != 'https':
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f'{field} must use https')



def _bearer_token(request) -> str | None:
    headers = getattr(request, 'headers', {}) or {}
    authz = headers.get('Authorization') or headers.get('authorization')
    if not authz:
        return None
    prefix, _, token = str(authz).partition(' ')
    if prefix.lower() != 'bearer' or not token:
        return None
    return token.strip() or None



def _validated_token_endpoint_auth_method(payload: DynamicClientRegistrationIn, *, policy) -> None:
    method = str(payload.token_endpoint_auth_method or 'client_secret_basic')
    if method not in DEFAULT_TOKEN_ENDPOINT_AUTH_METHODS:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f'invalid_client_metadata: unsupported token_endpoint_auth_method {method!r}')
    if policy.fapi_mode and method not in set(policy.allowed_client_auth_methods):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            'invalid_client_metadata: FAPI clients must use private_key_jwt, tls_client_auth, or self_signed_tls_client_auth',
        )
    if method == PRIVATE_KEY_JWT_AUTH_METHOD:
        if not payload.jwks_uri:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, 'invalid_client_metadata: private_key_jwt requires jwks_uri')
        if payload.token_endpoint_auth_signing_alg and payload.token_endpoint_auth_signing_alg not in SUPPORTED_CLIENT_ASSERTION_SIGNING_ALGS:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f'invalid_client_metadata: unsupported token_endpoint_auth_signing_alg {payload.token_endpoint_auth_signing_alg!r}',
            )
    elif method == TLS_CLIENT_AUTH_METHOD:
        if not payload.tls_client_certificate_thumbprint:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, 'invalid_client_metadata: tls_client_auth requires tls_client_certificate_thumbprint')
    elif method == SELF_SIGNED_TLS_CLIENT_AUTH_METHOD:
        if not payload.self_signed_tls_client_certificate_thumbprint:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, 'invalid_client_metadata: self_signed_tls_client_auth requires self_signed_tls_client_certificate_thumbprint')



def _merge_registration_metadata(payload: DynamicClientRegistrationIn, *, derived_metadata: dict[str, object]) -> dict[str, object]:
    metadata = payload.model_dump()
    metadata.update(derived_metadata)
    metadata.setdefault('application_type', 'native' if derived_metadata.get('native_application') else 'web')
    if payload.token_endpoint_auth_method == PRIVATE_KEY_JWT_AUTH_METHOD:
        metadata.setdefault('token_endpoint_auth_signing_alg', SUPPORTED_CLIENT_ASSERTION_SIGNING_ALGS[0])
    if payload.tls_client_certificate_thumbprint:
        metadata['tls_client_certificate_thumbprint'] = payload.tls_client_certificate_thumbprint
    if payload.self_signed_tls_client_certificate_thumbprint:
        metadata['self_signed_tls_client_certificate_thumbprint'] = payload.self_signed_tls_client_certificate_thumbprint
    return metadata


async def _validated_registration_payload(
    *,
    db,
    payload: DynamicClientRegistrationIn,
    deployment=None,
) -> tuple[Tenant, dict[str, object]]:
    deployment = deployment if deployment is not None else resolve_deployment(settings)
    policy = runtime_security_profile(deployment)

    unsupported_grants = sorted(set(payload.grant_types) - set(policy.allowed_grant_types))
    if unsupported_grants:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f'invalid_client_metadata: unsupported grant_types {unsupported_grants}')
    unsupported_response_types = sorted(set(payload.response_types) - set(policy.allowed_response_types))
    if unsupported_response_types:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f'invalid_client_metadata: unsupported response_types {unsupported_response_types}')

    tenant = await _resolve_registration_tenant(db=db, tenant_slug=payload.tenant_slug)

    redirect_uris = list(payload.redirect_uris or [])
    if not redirect_uris:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'redirect_uris required')
    for uri in redirect_uris:
        parsed = urlparse(uri)
        if is_native_redirect_uri(uri):
            validate_native_redirect_uri(uri)
            continue
        if parsed.scheme != 'https':
            raise HTTPException(status.HTTP_400_BAD_REQUEST, 'redirect_uris must use https')

    try:
        derived_metadata = validate_native_client_metadata(
            redirect_uris=redirect_uris,
            response_types=payload.response_types,
            grant_types=payload.grant_types,
        )
    except ValueError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f'invalid_client_metadata: {exc}') from exc

    _validated_token_endpoint_auth_method(payload, policy=policy)

    for uri in payload.post_logout_redirect_uris or []:
        _require_https_uri(uri, field='post_logout_redirect_uris')
    if payload.frontchannel_logout_uri:
        _require_https_uri(payload.frontchannel_logout_uri, field='frontchannel_logout_uri')
    if payload.backchannel_logout_uri:
        _require_https_uri(payload.backchannel_logout_uri, field='backchannel_logout_uri')
    return tenant, derived_metadata


async def _load_client_and_registration(*, db, client_id: str) -> tuple[UUID, Client | None, ClientRegistration | None]:
    try:
        client_uuid = UUID(str(client_id))
    except ValueError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'invalid client_id') from exc
    client = await read_handler_record(Client, db, client_uuid)
    registration = await first_handler_record(ClientRegistration, db, {"client_id": client_uuid})
    return client_uuid, client, registration


async def _require_registration_access(*, request, db, client_id: str) -> tuple[UUID, Client, ClientRegistration, str]:
    if not settings.enable_rfc7592:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'dynamic client registration management disabled')
    client_uuid, client, registration = await _load_client_and_registration(db=db, client_id=client_id)
    if client is None or registration is None or registration.disabled_at is not None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'client registration not found')
    bearer = _bearer_token(request)
    if not bearer:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            {'error': 'invalid_token', 'error_description': 'registration access token required'},
        )
    if not registration.registration_access_token_hash or token_hash(bearer) != registration.registration_access_token_hash:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            {'error': 'invalid_token', 'error_description': 'invalid registration access token'},
        )
    return client_uuid, client, registration, bearer


async def _registration_response(
    *,
    db,
    client: Client,
    registration: ClientRegistration,
    registration_access_token: str | None = None,
    client_secret: str | None = None,
) -> dict:
    metadata = dict(registration.registration_metadata or {})
    tenant = await read_handler_record(Tenant, db, client.tenant_id)
    redirect_uris = list(metadata.get('redirect_uris') or (client.redirect_uris or '').split())
    grant_types = list(metadata.get('grant_types') or (client.grant_types or 'authorization_code').split())
    response_types = list(metadata.get('response_types') or (client.response_types or 'code').split())
    issued_at = registration.issued_at
    if issued_at is not None and issued_at.tzinfo is None:
        issued_at = issued_at.replace(tzinfo=timezone.utc)
    return DynamicClientRegistrationOut(
        client_id=str(client.id),
        client_secret=client_secret,
        client_id_issued_at=int((issued_at or datetime.now(timezone.utc)).timestamp()),
        client_secret_expires_at=0,
        redirect_uris=redirect_uris,
        grant_types=grant_types,
        response_types=response_types,
        token_endpoint_auth_method=metadata.get('token_endpoint_auth_method', 'client_secret_basic'),
        token_endpoint_auth_signing_alg=metadata.get('token_endpoint_auth_signing_alg'),
        tls_client_certificate_thumbprint=metadata.get('tls_client_certificate_thumbprint'),
        self_signed_tls_client_certificate_thumbprint=metadata.get('self_signed_tls_client_certificate_thumbprint'),
        application_type=metadata.get('application_type'),
        scope=metadata.get('scope'),
        client_name=metadata.get('client_name'),
        client_uri=metadata.get('client_uri'),
        jwks_uri=metadata.get('jwks_uri'),
        contacts=metadata.get('contacts'),
        software_id=metadata.get('software_id'),
        software_version=metadata.get('software_version'),
        post_logout_redirect_uris=metadata.get('post_logout_redirect_uris'),
        frontchannel_logout_uri=metadata.get('frontchannel_logout_uri'),
        frontchannel_logout_session_required=metadata.get('frontchannel_logout_session_required', True),
        backchannel_logout_uri=metadata.get('backchannel_logout_uri'),
        backchannel_logout_session_required=metadata.get('backchannel_logout_session_required', True),
        registration_access_token=registration_access_token,
        registration_client_uri=registration.registration_client_uri,
    ).model_dump(exclude_none=True)


