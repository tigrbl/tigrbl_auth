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
from tigrbl_identity_runtime.deployment import (
    deployment_from_app,
    deployment_from_request,
    resolve_deployment,
)
from tigrbl_identity_runtime.settings import settings
from tigrbl_identity_storage.framework import (
    Depends,
    HTTPException,
    TigrblApp,
    TigrblRouter,
    status,
)
from tigrbl_identity_storage.tables._ops import (
    create_record,
    first_record,
    read_record,
    token_hash,
    update_record,
)
from tigrbl_identity_storage.tables.audit_event import AuditEvent
from tigrbl_identity_storage.tables.engine import get_db
from tigrbl_identity_storage_runtime.tenant_state import enabled_tenant_record
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
from tigrbl_identity_storage.tables.client import Client
from tigrbl_identity_jose.key_management import hash_pw
from tigrbl_identity_storage.tables.tenant import Tenant


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

api = router = TigrblRouter()


from ._client_registration_validation import (
    _bearer_token, _merge_registration_metadata, _resolve_registration_tenant,
    _validated_registration_payload,
)

async def _load_client_and_registration(
    *, db, client_id: str
) -> tuple[UUID, Client | None, ClientRegistration | None]:
    try:
        client_uuid = UUID(str(client_id))
    except ValueError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "invalid client_id") from exc
    client = await read_record(Client, db, client_uuid)
    registration = await first_record(
        ClientRegistration, db, {"client_id": client_uuid}
    )
    return client_uuid, client, registration


async def _require_registration_access(
    *, request, db, client_id: str
) -> tuple[UUID, Client, ClientRegistration, str]:
    if not settings.enable_rfc7592:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "dynamic client registration management disabled"
        )
    client_uuid, client, registration = await _load_client_and_registration(
        db=db, client_id=client_id
    )
    if client is None or registration is None or registration.disabled_at is not None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "client registration not found")
    bearer = _bearer_token(request)
    if not bearer:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            {
                "error": "invalid_token",
                "error_description": "registration access token required",
            },
        )
    if (
        not registration.registration_access_token_hash
        or token_hash(bearer) != registration.registration_access_token_hash
    ):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            {
                "error": "invalid_token",
                "error_description": "invalid registration access token",
            },
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
    await read_record(Tenant, db, client.tenant_id)
    redirect_uris = list(
        metadata.get("redirect_uris") or (client.redirect_uris or "").split()
    )
    grant_types = list(
        metadata.get("grant_types")
        or (client.grant_types or "authorization_code").split()
    )
    response_types = list(
        metadata.get("response_types") or (client.response_types or "code").split()
    )
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
        contacts=metadata.get("contacts"),
        software_id=metadata.get("software_id"),
        software_version=metadata.get("software_version"),
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
        registration_client_uri=registration.registration_client_uri,
    ).model_dump(exclude_none=True)


async def register_client(
    *, request, db, payload: DynamicClientRegistrationIn | None = None
):
    if not settings.enable_rfc7591:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "dynamic client registration disabled"
        )
    if payload is None:
        body = await request.json() if hasattr(request, "json") else {}
        payload = DynamicClientRegistrationIn(**body)

    deployment = deployment_from_request(request, settings)
    tenant, derived_metadata = await _validated_registration_payload(
        db=db, payload=payload, deployment=deployment
    )
    policy = runtime_security_profile(deployment)

    client_id = str(uuid4())
    client_secret = secrets.token_urlsafe(32)
    client = await create_record(
        Client,
        db,
        {
            "id": UUID(client_id),
            "tenant_id": tenant.id,
            "client_secret_hash": hash_pw(client_secret),
            "redirect_uris": list(payload.redirect_uris),
            "grant_types": " ".join(payload.grant_types),
            "response_types": " ".join(payload.response_types),
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
            "client_id": client.id,
            "tenant_id": tenant.id,
            "registration_metadata": metadata,
            "contacts": payload.contacts,
            "software_id": payload.software_id,
            "software_version": payload.software_version,
            "registration_access_token_hash": registration_access_token_hash,
            "registration_client_uri": registration_client_uri,
        },
    )
    await create_record(
        AuditEvent,
        db,
        {
            "tenant_id": tenant.id,
            "actor_client_id": client.id,
            "event_type": "client.registration.created",
            "target_type": "client",
            "target_id": str(client.id),
            "details": {
                "redirect_uris": list(payload.redirect_uris),
                "grant_types": list(payload.grant_types),
                "response_types": list(payload.response_types),
                "token_endpoint_auth_method": payload.token_endpoint_auth_method,
                "token_endpoint_auth_signing_alg": payload.token_endpoint_auth_signing_alg,
                "tls_client_certificate_thumbprint": payload.tls_client_certificate_thumbprint,
                "self_signed_tls_client_certificate_thumbprint": payload.self_signed_tls_client_certificate_thumbprint,
                "tls_client_auth_subject_dn": payload.tls_client_auth_subject_dn,
                "tls_client_auth_san_dns": payload.tls_client_auth_san_dns,
                "tls_client_auth_san_uri": payload.tls_client_auth_san_uri,
                "tls_client_auth_san_ip": payload.tls_client_auth_san_ip,
                "tls_client_auth_san_email": payload.tls_client_auth_san_email,
                "application_type": metadata.get("application_type"),
                "native_application": metadata.get("native_application", False),
                "pkce_required": metadata.get("pkce_required", False),
                "post_logout_redirect_uris": payload.post_logout_redirect_uris,
                "frontchannel_logout_uri": payload.frontchannel_logout_uri,
                "backchannel_logout_uri": payload.backchannel_logout_uri,
            },
        },
    )

    return await _registration_response(
        db=db,
        client=client,
        registration=registration,
        registration_access_token=registration_access_token,
        client_secret=None
        if policy.fapi_mode
        and payload.token_endpoint_auth_method
        in set(policy.allowed_client_auth_methods)
        else client_secret,
    )


