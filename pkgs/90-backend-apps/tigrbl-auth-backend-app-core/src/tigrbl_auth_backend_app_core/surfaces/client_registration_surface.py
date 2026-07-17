"""Runtime security, policy, and composition for RFC 7591 and RFC 7592."""

from __future__ import annotations

import secrets
from pathlib import Path
from uuid import UUID, uuid4

from tigrbl import Request, TigrblApp
from tigrbl.runtime.status import HTTPException, status
from tigrbl_auth_router_oauth_registration import (
    build_client_registration_router,
    include_client_registration_endpoint as include_http_registration_endpoint,
)
from tigrbl_auth_protocol_oauth.schemas import (
    DynamicClientRegistrationIn,
    DynamicClientRegistrationManagementIn,
)
from tigrbl_auth_protocol_oauth.standards.client_registration_management import (
    RFC7592ClientRegistrationManagementService,
)
from tigrbl_auth_protocol_oauth.standards.dynamic_client_registration import (
    RFC7591DynamicClientRegistrationService,
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
from tigrbl_secret_hashing_bcrypt_provider import hash_pw
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

from tigrbl_identity_server.security.client_registration import (
    build_client_registration_capability,
)
from tigrbl_identity_server.client_registration_support import (
    bearer_token as _bearer_token,
    merge_registration_metadata as _merge_registration_metadata,
    registration_response as _registration_response,
    validate_registration_metadata,
    validate_token_endpoint_auth_method as _validated_token_endpoint_auth_method,
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
        str(record.get("name") or data.get("name") or "Tenant").strip() or "Tenant"
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


async def _validated_registration_payload(
    *,
    db,
    payload: DynamicClientRegistrationIn,
    deployment=None,
) -> tuple[Tenant, dict[str, object]]:
    deployment = deployment if deployment is not None else resolve_deployment(settings)
    policy = runtime_security_profile(deployment)
    tenant = await _resolve_registration_tenant(
        db=db,
        tenant_slug=payload.tenant_slug,
    )
    derived_metadata = validate_registration_metadata(payload, policy=policy)
    return tenant, derived_metadata


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
