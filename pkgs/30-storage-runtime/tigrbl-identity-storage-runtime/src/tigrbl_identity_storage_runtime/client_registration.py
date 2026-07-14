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


from ._client_registration_create import register_client
from ._client_registration_management import (
    delete_registered_client, get_registered_client, update_registered_client,
)

def _repo_root() -> Path:
    return Path(__file__).resolve().parents[5]


def _sync_client_registration(command: str, registration: object) -> None:
    from tigrbl_identity_storage_runtime.operator_store import OperationContext
    from tigrbl_identity_storage_runtime.resource_service import (
        create_resource,
        delete_resource,
        update_resource,
    )

    if isinstance(registration, dict):
        payload = dict(registration)
    elif hasattr(registration, "model_dump"):
        payload = registration.model_dump(mode="json")
    else:
        payload = dict(getattr(registration, "__dict__", {}))
    client_id = str(payload.get("client_id") or payload.get("id"))
    if not client_id:
        return
    context = OperationContext(
        repo_root=_repo_root(), command=command, resource="client", actor="rest"
    )
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
    existing_command = (
        update_resource if command.endswith(".update") else create_resource
    )
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
            update_resource(
                context, record_id=client_id, patch=patch, if_missing="create"
            )
        else:
            create_resource(
                context, record_id=client_id, patch=patch, if_exists="update"
            )


@api.route("/register", methods=["POST"], response_model=DynamicClientRegistrationOut)
async def register(request, db=Depends(get_db)):
    result = await register_client(request=request, db=db)
    _sync_client_registration("client.registration.create", result)
    return result


@api.route(
    "/register/{client_id}",
    methods=["GET"],
    response_model=DynamicClientRegistrationOut,
)
async def register_get(request, client_id: str, db=Depends(get_db)):
    return await get_registered_client(request=request, db=db, client_id=client_id)


@api.route(
    "/register/{client_id}",
    methods=["PUT"],
    response_model=DynamicClientRegistrationOut,
)
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
