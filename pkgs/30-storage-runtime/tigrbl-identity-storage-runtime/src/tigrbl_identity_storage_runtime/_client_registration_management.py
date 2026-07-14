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
from .ops.common import (
    create_record,
    first_record,
    read_record,
    token_hash,
    update_record,
)
from tigrbl_identity_storage.tables.audit_event import AuditEvent
from .engine import get_db
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


from ._client_registration_create import (
    _load_client_and_registration, _registration_response, _require_registration_access,
)
from ._client_registration_validation import (
    _bearer_token, _merge_registration_metadata, _validated_registration_payload,
)

async def get_registered_client(*, request, db, client_id: str):
    _, client, registration, bearer = await _require_registration_access(
        request=request, db=db, client_id=client_id
    )
    return await _registration_response(
        db=db,
        client=client,
        registration=registration,
        registration_access_token=bearer,
    )


async def update_registered_client(
    *,
    request,
    db,
    client_id: str,
    payload: DynamicClientRegistrationManagementIn | None = None,
):
    _, client, registration, bearer = await _require_registration_access(
        request=request, db=db, client_id=client_id
    )
    if payload is None:
        body = await request.json() if hasattr(request, "json") else {}
        payload = DynamicClientRegistrationManagementIn(**body)

    current = dict(registration.registration_metadata or {})
    tenant = await read_record(Tenant, db, client.tenant_id)
    current.setdefault("tenant_slug", tenant.slug if tenant is not None else "public")
    current.setdefault("redirect_uris", (client.redirect_uris or "").split())
    current.setdefault(
        "grant_types", (client.grant_types or "authorization_code").split()
    )
    current.setdefault("response_types", (client.response_types or "code").split())
    current.setdefault("token_endpoint_auth_method", "client_secret_basic")

    incoming = payload.model_dump(exclude_none=True)
    current.update(incoming)
    validated = DynamicClientRegistrationIn(**current)
    deployment = deployment_from_request(request, settings)
    _, derived_metadata = await _validated_registration_payload(
        db=db, payload=validated, deployment=deployment
    )

    client = await update_record(
        Client,
        db,
        client.id,
        {
            "redirect_uris": " ".join(validated.redirect_uris),
            "grant_types": " ".join(validated.grant_types),
            "response_types": " ".join(validated.response_types),
        },
    )

    metadata = _merge_registration_metadata(
        validated, derived_metadata=derived_metadata
    )
    registration = await update_record(
        ClientRegistration,
        db,
        registration.id,
        {
            "registration_metadata": metadata,
            "contacts": validated.contacts,
            "software_id": validated.software_id,
            "software_version": validated.software_version,
            "registration_access_token_hash": registration.registration_access_token_hash,
            "registration_client_uri": registration.registration_client_uri,
        },
    )
    await create_record(
        AuditEvent,
        db,
        {
            "tenant_id": client.tenant_id,
            "actor_client_id": client.id,
            "event_type": "client.registration.updated",
            "target_type": "client",
            "target_id": str(client.id),
            "details": {
                "updated_fields": sorted(incoming.keys()),
                "token_endpoint_auth_method": metadata.get(
                    "token_endpoint_auth_method"
                ),
                "token_endpoint_auth_signing_alg": metadata.get(
                    "token_endpoint_auth_signing_alg"
                ),
                "tls_client_certificate_thumbprint": metadata.get(
                    "tls_client_certificate_thumbprint"
                ),
                "self_signed_tls_client_certificate_thumbprint": metadata.get(
                    "self_signed_tls_client_certificate_thumbprint"
                ),
                "tls_client_auth_subject_dn": metadata.get(
                    "tls_client_auth_subject_dn"
                ),
                "tls_client_auth_san_dns": metadata.get("tls_client_auth_san_dns"),
                "tls_client_auth_san_uri": metadata.get("tls_client_auth_san_uri"),
                "tls_client_auth_san_ip": metadata.get("tls_client_auth_san_ip"),
                "tls_client_auth_san_email": metadata.get("tls_client_auth_san_email"),
                "application_type": metadata.get("application_type"),
                "native_application": metadata.get("native_application", False),
                "pkce_required": metadata.get("pkce_required", False),
            },
        },
    )
    return await _registration_response(
        db=db,
        client=client,
        registration=registration,
        registration_access_token=bearer,
    )


async def delete_registered_client(*, request, db, client_id: str):
    _, client, registration, _ = await _require_registration_access(
        request=request, db=db, client_id=client_id
    )
    disabled_at = datetime.now(timezone.utc)
    await update_record(
        ClientRegistration, db, registration.id, {"disabled_at": disabled_at}
    )
    await update_record(Client, db, client.id, {"is_active": False})
    await create_record(
        AuditEvent,
        db,
        {
            "tenant_id": client.tenant_id,
            "actor_client_id": None,
            "event_type": "client.registration.deleted",
            "target_type": "client",
            "target_id": str(client.id),
            "details": {
                "registration_client_uri": registration.registration_client_uri
            },
        },
    )
    return {"status": "deleted", "client_id": str(client.id)}


