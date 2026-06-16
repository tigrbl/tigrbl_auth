"""OpenID Connect discovery and JWKS endpoints with profile-aware policy metadata."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from tigrbl_identity_server.framework import Depends, HTTPException, Request, TigrblApp, TigrblRouter, status
from tigrbl_identity_runtime.deployment import (
    ResolvedDeployment,
    deployment_from_app,
    deployment_from_request,
    resolve_deployment,
)
from tigrbl_identity_server.security.handler_records import first_handler_record
from tigrbl_identity_runtime.settings import settings
from tigrbl_identity_operator.operator_service import build_operator_jwks_payload, get_record
from tigrbl_identity_principals.tenant_discovery import (
    REALM_JWKS_PATH,
    REALM_OPENID_CONFIGURATION_PATH,
    TENANT_JWKS_PATH,
    TENANT_OPENID_CONFIGURATION_PATH,
    build_realm_openid_config,
    build_tenant_openid_config,
)
from tigrbl_identity_jose.jwks_service import build_jwks_document
from tigrbl_auth_protocol_oidc.standards.discovery_metadata import build_openid_config
from tigrbl_identity_runtime.http_standards.well_known import WELL_KNOWN_ENDPOINTS
from tigrbl_auth_protocol_oauth.standards.rfc8414_metadata import ISSUER, JWKS_PATH
from tigrbl_auth_protocol_oauth.standards.rfc9700 import discovery_policy_metadata
from tigrbl_identity_storage.tables import Realm, Tenant
from tigrbl_identity_storage.tables.engine import get_db

api = TigrblRouter()
discovery_api = TigrblRouter()
jwks_api = TigrblRouter()
router = api
api.include_router(discovery_api)
api.include_router(jwks_api)


def _settings_signature(
    settings_obj: object | None = None,
    *,
    profile: str | None = None,
    flag_overrides: dict[str, Any] | None = None,
) -> str:
    deployment = resolve_deployment(settings_obj or settings, profile=profile, flag_overrides=flag_overrides)
    return json.dumps(deployment.to_manifest(), sort_keys=True)


def _build_openid_config(
    settings_obj: object | ResolvedDeployment | None = None,
    *,
    profile: str | None = None,
    flag_overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return build_openid_config(settings_obj or settings, profile=profile, flag_overrides=flag_overrides)


@lru_cache(maxsize=8)
def _cached_openid_config(sig: str) -> dict[str, Any]:
    try:
        manifest = json.loads(sig)
        if isinstance(manifest, dict):
            deployment = ResolvedDeployment(**manifest)
            return _build_openid_config(deployment)
    except Exception:
        pass
    return _build_openid_config()


def refresh_discovery_cache() -> None:
    _cached_openid_config.cache_clear()


@discovery_api.route("/.well-known/openid-configuration", methods=["GET"], tags=[".well-known"])
async def openid_configuration(request: Request):
    deployment = deployment_from_request(request, settings)
    if not deployment.route_enabled("/.well-known/openid-configuration"):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "OIDC discovery disabled")
    return build_openid_config(deployment)


@discovery_api.route(
    "/.well-known/openid-configuration",
    methods=["POST", "PUT", "PATCH", "DELETE"],
    include_in_schema=False,
    tags=[".well-known"],
)
async def openid_configuration_method_not_allowed(request: Request):
    raise HTTPException(status.HTTP_405_METHOD_NOT_ALLOWED, "method not allowed")


async def _tenant_exists(*, db, tenant_slug: str) -> bool:
    if tenant_slug == "public":
        return True
    operator_record = get_record(Path.cwd(), "tenant", tenant_slug)
    operator_fallback = _tenant_record_enabled(operator_record)
    if db is None:
        return operator_fallback
    try:
        tenant = await first_handler_record(Tenant, db, {"slug": tenant_slug})
    except Exception:
        return operator_fallback
    if tenant is not None:
        return True
    return operator_fallback


def _tenant_record_enabled(record: dict[str, Any] | None) -> bool:
    if record is None:
        return False
    status_value = str(record.get("status") or "").lower()
    if status_value in {"deleted", "disabled", "revoked"}:
        return False
    return record.get("enabled") is not False


async def _realm_exists(*, db, realm_slug: str) -> bool:
    if realm_slug == "default":
        return True
    if db is None:
        return False
    try:
        realm = await first_handler_record(Realm, db, {"slug": realm_slug})
    except Exception:
        return False
    return realm is not None


@discovery_api.route(TENANT_OPENID_CONFIGURATION_PATH, methods=["GET"], tags=[".well-known", "tenant"])
async def tenant_openid_configuration(request: Request, tenant_slug: str, db=Depends(get_db)):
    deployment = deployment_from_request(request, settings)
    if not deployment.route_enabled(TENANT_OPENID_CONFIGURATION_PATH):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Tenant OIDC discovery disabled")
    if not await _tenant_exists(db=db, tenant_slug=tenant_slug):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Tenant not found")
    return build_tenant_openid_config(deployment, tenant_slug)


@discovery_api.route(REALM_OPENID_CONFIGURATION_PATH, methods=["GET"], tags=[".well-known", "realm"])
async def realm_openid_configuration(request: Request, realm_slug: str, db=Depends(get_db)):
    deployment = deployment_from_request(request, settings)
    if not deployment.route_enabled(REALM_OPENID_CONFIGURATION_PATH):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Realm OIDC discovery disabled")
    if not await _realm_exists(db=db, realm_slug=realm_slug):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Realm not found")
    return build_realm_openid_config(deployment, realm_slug)


@jwks_api.route(JWKS_PATH, methods=["GET"], tags=[".well-known"])
async def jwks(request: Request):
    deployment = deployment_from_request(request, settings)
    if not deployment.route_enabled(JWKS_PATH):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "JWKS publication disabled")
    return await build_jwks_document()


@jwks_api.route(
    JWKS_PATH,
    methods=["POST", "PUT", "PATCH", "DELETE"],
    include_in_schema=False,
    tags=[".well-known"],
)
async def jwks_method_not_allowed(request: Request):
    raise HTTPException(status.HTTP_405_METHOD_NOT_ALLOWED, "method not allowed")


@jwks_api.route(TENANT_JWKS_PATH, methods=["GET"], tags=[".well-known", "tenant"])
async def tenant_jwks(request: Request, tenant_slug: str, db=Depends(get_db)):
    deployment = deployment_from_request(request, settings)
    if not deployment.route_enabled(TENANT_JWKS_PATH):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Tenant JWKS publication disabled")
    if not await _tenant_exists(db=db, tenant_slug=tenant_slug):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Tenant not found")
    return build_operator_jwks_payload(Path.cwd(), tenant=tenant_slug)


@jwks_api.route(REALM_JWKS_PATH, methods=["GET"], tags=[".well-known", "realm"])
async def realm_jwks(request: Request, realm_slug: str, db=Depends(get_db)):
    deployment = deployment_from_request(request, settings)
    if not deployment.route_enabled(REALM_JWKS_PATH):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Realm JWKS publication disabled")
    if not await _realm_exists(db=db, realm_slug=realm_slug):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Realm not found")
    return build_operator_jwks_payload(Path.cwd(), tenant=realm_slug)


def _include_if_missing(app: TigrblApp, router_obj: TigrblRouter, path: str) -> None:
    if not any((getattr(route, "path", None) or getattr(route, "path_template", None)) == path for route in app.router.routes):
        app.include_router(router_obj)


def include_openid_configuration(app: TigrblApp) -> None:
    deployment = deployment_from_app(app, settings)
    path = "/.well-known/openid-configuration"
    if deployment.route_enabled(path):
        _include_if_missing(app, discovery_api, path)


def include_jwks(app: TigrblApp) -> None:
    deployment = deployment_from_app(app, settings)
    if deployment.route_enabled(JWKS_PATH):
        _include_if_missing(app, jwks_api, JWKS_PATH)


def include_oidc_discovery(app: TigrblApp) -> None:
    include_openid_configuration(app)
    include_jwks(app)


__all__ = [
    "JWKS_PATH",
    "ISSUER",
    "api",
    "discovery_api",
    "jwks_api",
    "router",
    "include_openid_configuration",
    "include_jwks",
    "include_oidc_discovery",
    "refresh_discovery_cache",
    "_build_openid_config",
    "_cached_openid_config",
    "_settings_signature",
]
