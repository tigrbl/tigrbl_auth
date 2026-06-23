from __future__ import annotations

import secrets
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from uuid import UUID, uuid4

from tigrbl_identity_storage.tables.client_registration import (
    ClientRegistration,
    DynamicClientRegistrationIn,
    DynamicClientRegistrationManagementIn,
    DynamicClientRegistrationOut,
)
from tigrbl_identity_runtime.deployment import deployment_from_app, deployment_from_request, resolve_deployment
from tigrbl_identity_runtime.settings import settings
from tigrbl_identity_storage.framework import Depends, HTTPException, TigrblApp, TigrblRouter, status
from tigrbl_identity_storage.tables._ops import (
    create_record,
    first_record,
    read_record,
    token_hash,
    update_record,
)
from tigrbl_identity_storage.tables.audit_event import AuditEvent
from tigrbl_identity_storage.tables.engine import get_db
from tigrbl_identity_storage.tables.tenant import enabled_tenant_record
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
from tigrbl_auth_protocol_oauth.standards.oauth_security_bcp import runtime_security_profile
from tigrbl_identity_storage.tables.client import Client
from tigrbl_identity_storage.tables.tenant import Tenant


DEFAULT_TOKEN_ENDPOINT_AUTH_METHODS = {"client_secret_basic", "client_secret_post", PRIVATE_KEY_JWT_AUTH_METHOD, *SUPPORTED_MTLS_AUTH_METHODS}
TLS_CLIENT_AUTH_IDENTITY_FIELDS = (
    "tls_client_auth_subject_dn",
    "tls_client_auth_san_dns",
    "tls_client_auth_san_uri",
    "tls_client_auth_san_ip",
    "tls_client_auth_san_email",
)

api = router = TigrblRouter()


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
    tenant = await first_record(Tenant, db, {"slug": tenant_slug})
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
        tenant = await create_record(Tenant, db, payload)
    except Exception as exc:
        tenant = await first_record(Tenant, db, {"slug": tenant_slug})
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
        has_identity_metadata = any(getattr(payload, field, None) for field in TLS_CLIENT_AUTH_IDENTITY_FIELDS)
        if not payload.tls_client_certificate_thumbprint and not has_identity_metadata:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                'invalid_client_metadata: tls_client_auth requires tls_client_certificate_thumbprint, subject_dn, or SAN metadata',
            )
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
    client = await read_record(Client, db, client_uuid)
    registration = await first_record(ClientRegistration, db, {"client_id": client_uuid})
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
    tenant = await read_record(Tenant, db, client.tenant_id)
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
        tls_client_auth_subject_dn=metadata.get('tls_client_auth_subject_dn'),
        tls_client_auth_san_dns=metadata.get('tls_client_auth_san_dns'),
        tls_client_auth_san_uri=metadata.get('tls_client_auth_san_uri'),
        tls_client_auth_san_ip=metadata.get('tls_client_auth_san_ip'),
        tls_client_auth_san_email=metadata.get('tls_client_auth_san_email'),
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


async def register_client(*, request, db, payload: DynamicClientRegistrationIn | None = None):
    if not settings.enable_rfc7591:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'dynamic client registration disabled')
    if payload is None:
        body = await request.json() if hasattr(request, 'json') else {}
        payload = DynamicClientRegistrationIn(**body)

    deployment = deployment_from_request(request, settings)
    tenant, derived_metadata = await _validated_registration_payload(db=db, payload=payload, deployment=deployment)
    policy = runtime_security_profile(deployment)

    client_id = str(uuid4())
    client_secret = secrets.token_urlsafe(32)
    client_seed = Client.new(tenant.id, client_id, client_secret, list(payload.redirect_uris))
    client = await create_record(
        Client,
        db,
        {
            'id': client_seed.id,
            'tenant_id': tenant.id,
            'client_secret_hash': client_seed.client_secret_hash,
            'redirect_uris': client_seed.redirect_uris,
            'grant_types': ' '.join(payload.grant_types),
            'response_types': ' '.join(payload.response_types),
        },
    )

    registration_access_token = None
    registration_client_uri = None
    registration_access_token_hash = None
    if settings.enable_rfc7592:
        registration_access_token = secrets.token_urlsafe(32)
        registration_access_token_hash = token_hash(registration_access_token)
        registration_client_uri = f"{str(deployment.issuer or settings.issuer).rstrip('/')}/register/{client_id}"

    metadata = _merge_registration_metadata(payload, derived_metadata=derived_metadata)
    registration = await create_record(
        ClientRegistration,
        db,
        {
            'client_id': client.id,
            'tenant_id': tenant.id,
            'registration_metadata': metadata,
            'contacts': payload.contacts,
            'software_id': payload.software_id,
            'software_version': payload.software_version,
            'registration_access_token_hash': registration_access_token_hash,
            'registration_client_uri': registration_client_uri,
        },
    )
    await AuditEvent.record(
        db,
        tenant_id=tenant.id,
        actor_client_id=client.id,
        event_type='client.registration.created',
        target_type='client',
        target_id=str(client.id),
        details={
            'redirect_uris': list(payload.redirect_uris),
            'grant_types': list(payload.grant_types),
            'response_types': list(payload.response_types),
            'token_endpoint_auth_method': payload.token_endpoint_auth_method,
            'token_endpoint_auth_signing_alg': payload.token_endpoint_auth_signing_alg,
            'tls_client_certificate_thumbprint': payload.tls_client_certificate_thumbprint,
            'self_signed_tls_client_certificate_thumbprint': payload.self_signed_tls_client_certificate_thumbprint,
            'tls_client_auth_subject_dn': payload.tls_client_auth_subject_dn,
            'tls_client_auth_san_dns': payload.tls_client_auth_san_dns,
            'tls_client_auth_san_uri': payload.tls_client_auth_san_uri,
            'tls_client_auth_san_ip': payload.tls_client_auth_san_ip,
            'tls_client_auth_san_email': payload.tls_client_auth_san_email,
            'application_type': metadata.get('application_type'),
            'native_application': metadata.get('native_application', False),
            'pkce_required': metadata.get('pkce_required', False),
            'post_logout_redirect_uris': payload.post_logout_redirect_uris,
            'frontchannel_logout_uri': payload.frontchannel_logout_uri,
            'backchannel_logout_uri': payload.backchannel_logout_uri,
        },
    )

    return await _registration_response(
        db=db,
        client=client,
        registration=registration,
        registration_access_token=registration_access_token,
        client_secret=None if policy.fapi_mode and payload.token_endpoint_auth_method in set(policy.allowed_client_auth_methods) else client_secret,
    )


async def get_registered_client(*, request, db, client_id: str):
    _, client, registration, bearer = await _require_registration_access(request=request, db=db, client_id=client_id)
    return await _registration_response(db=db, client=client, registration=registration, registration_access_token=bearer)


async def update_registered_client(
    *,
    request,
    db,
    client_id: str,
    payload: DynamicClientRegistrationManagementIn | None = None,
):
    _, client, registration, bearer = await _require_registration_access(request=request, db=db, client_id=client_id)
    if payload is None:
        body = await request.json() if hasattr(request, 'json') else {}
        payload = DynamicClientRegistrationManagementIn(**body)

    current = dict(registration.registration_metadata or {})
    tenant = await read_record(Tenant, db, client.tenant_id)
    current.setdefault('tenant_slug', tenant.slug if tenant is not None else 'public')
    current.setdefault('redirect_uris', (client.redirect_uris or '').split())
    current.setdefault('grant_types', (client.grant_types or 'authorization_code').split())
    current.setdefault('response_types', (client.response_types or 'code').split())
    current.setdefault('token_endpoint_auth_method', 'client_secret_basic')

    incoming = payload.model_dump(exclude_none=True)
    current.update(incoming)
    validated = DynamicClientRegistrationIn(**current)
    deployment = deployment_from_request(request, settings)
    _, derived_metadata = await _validated_registration_payload(db=db, payload=validated, deployment=deployment)

    client = await update_record(
        Client,
        db,
        client.id,
        {
            'redirect_uris': ' '.join(validated.redirect_uris),
            'grant_types': ' '.join(validated.grant_types),
            'response_types': ' '.join(validated.response_types),
        },
    )

    metadata = _merge_registration_metadata(validated, derived_metadata=derived_metadata)
    registration = await update_record(
        ClientRegistration,
        db,
        registration.id,
        {
            'registration_metadata': metadata,
            'contacts': validated.contacts,
            'software_id': validated.software_id,
            'software_version': validated.software_version,
            'registration_access_token_hash': registration.registration_access_token_hash,
            'registration_client_uri': registration.registration_client_uri,
        },
    )
    await AuditEvent.record(
        db,
        tenant_id=client.tenant_id,
        actor_client_id=client.id,
        event_type='client.registration.updated',
        target_type='client',
        target_id=str(client.id),
        details={
            'updated_fields': sorted(incoming.keys()),
            'token_endpoint_auth_method': metadata.get('token_endpoint_auth_method'),
            'token_endpoint_auth_signing_alg': metadata.get('token_endpoint_auth_signing_alg'),
            'tls_client_certificate_thumbprint': metadata.get('tls_client_certificate_thumbprint'),
            'self_signed_tls_client_certificate_thumbprint': metadata.get('self_signed_tls_client_certificate_thumbprint'),
            'tls_client_auth_subject_dn': metadata.get('tls_client_auth_subject_dn'),
            'tls_client_auth_san_dns': metadata.get('tls_client_auth_san_dns'),
            'tls_client_auth_san_uri': metadata.get('tls_client_auth_san_uri'),
            'tls_client_auth_san_ip': metadata.get('tls_client_auth_san_ip'),
            'tls_client_auth_san_email': metadata.get('tls_client_auth_san_email'),
            'application_type': metadata.get('application_type'),
            'native_application': metadata.get('native_application', False),
            'pkce_required': metadata.get('pkce_required', False),
        },
    )
    return await _registration_response(db=db, client=client, registration=registration, registration_access_token=bearer)


async def delete_registered_client(*, request, db, client_id: str):
    _, client, registration, _ = await _require_registration_access(request=request, db=db, client_id=client_id)
    disabled_at = datetime.now(timezone.utc)
    await update_record(ClientRegistration, db, registration.id, {'disabled_at': disabled_at})
    await update_record(Client, db, client.id, {'is_active': False})
    await AuditEvent.record(
        db,
        tenant_id=client.tenant_id,
        actor_client_id=None,
        event_type='client.registration.deleted',
        target_type='client',
        target_id=str(client.id),
        details={'registration_client_uri': registration.registration_client_uri},
    )
    return {'status': 'deleted', 'client_id': str(client.id)}


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[5]


def _sync_client_registration(command: str, registration: object) -> None:
    from tigrbl_identity_storage_runtime.operator_store import OperationContext
    from tigrbl_identity_storage_runtime.resource_service import create_resource, delete_resource, update_resource

    if isinstance(registration, dict):
        payload = dict(registration)
    elif hasattr(registration, "model_dump"):
        payload = registration.model_dump(mode="json")
    else:
        payload = dict(getattr(registration, "__dict__", {}))
    client_id = str(payload.get("client_id") or payload.get("id"))
    if not client_id:
        return
    context = OperationContext(repo_root=_repo_root(), command=command, resource="client", actor="rest")
    patch = {
        "client_id": client_id,
        "tenant_id": payload.get("tenant_id"),
        "metadata": payload,
        "contacts": payload.get("contacts") or [],
        "software_id": payload.get("software_id"),
        "software_version": payload.get("software_version"),
        "registration_access_token_hash": payload.get("registration_access_token_hash"),
        "registration_client_uri": payload.get("registration_client_uri"),
    }
    if command.endswith(".delete"):
        try:
            delete_resource(context, record_id=client_id, if_missing="skip")
        except Exception:
            pass
        return
    existing_command = update_resource if command.endswith(".update") else create_resource
    try:
        existing_command(
            context,
            record_id=client_id,
            patch=patch,
            if_missing="create" if command.endswith(".update") else "error",
            if_exists="update" if command.endswith(".create") else "error",
        )
    except TypeError:
        if command.endswith(".update"):
            update_resource(context, record_id=client_id, patch=patch, if_missing="create")
        else:
            create_resource(context, record_id=client_id, patch=patch, if_exists="update")


@api.route("/register", methods=["POST"], response_model=DynamicClientRegistrationOut)
async def register(request, db=Depends(get_db)):
    result = await register_client(request=request, db=db)
    _sync_client_registration("client.registration.create", result)
    return result


@api.route("/register/{client_id}", methods=["GET"], response_model=DynamicClientRegistrationOut)
async def register_get(request, client_id: str, db=Depends(get_db)):
    return await get_registered_client(request=request, db=db, client_id=client_id)


@api.route("/register/{client_id}", methods=["PUT"], response_model=DynamicClientRegistrationOut)
async def register_put(request, client_id: str, db=Depends(get_db)):
    result = await update_registered_client(request=request, db=db, client_id=client_id)
    _sync_client_registration("client.registration.update", result)
    return result


@api.route("/register/{client_id}", methods=["DELETE"])
async def register_delete(request, client_id: str, db=Depends(get_db)):
    result = await delete_registered_client(request=request, db=db, client_id=client_id)
    _sync_client_registration("client.registration.delete", {"client_id": client_id})
    return result


def include_client_registration_endpoint(app: TigrblApp) -> None:
    deployment = deployment_from_app(app, settings)
    paths = ("/register", "/register/{client_id}")
    if any(deployment.route_enabled(path) for path in paths) and not any(
        (getattr(route, "path", None) or getattr(route, "path_template", None)) in paths
        for route in app.router.routes
    ):
        app.include_router(api)


include_rfc7591 = include_client_registration_endpoint
include_rfc7592 = include_client_registration_endpoint


__all__ = [
    "api",
    "router",
    "register",
    "register_get",
    "register_put",
    "register_delete",
    "register_client",
    "get_registered_client",
    "update_registered_client",
    "delete_registered_client",
    "include_client_registration_endpoint",
    "include_rfc7591",
    "include_rfc7592",
    "_merge_registration_metadata",
    "_registration_response",
    "_require_registration_access",
    "_validated_registration_payload",
    "_validated_token_endpoint_auth_method",
]
