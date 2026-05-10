"""OpenID Connect discovery and JWKS endpoints with profile-aware policy metadata."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from tigrbl_auth.framework import HTTPException, Request, TigrblApp, TigrblRouter, status
from tigrbl_auth.config.deployment import (
    ResolvedDeployment,
    deployment_from_app,
    deployment_from_request,
    resolve_deployment,
)
from tigrbl_auth.config.settings import settings
from tigrbl_auth.services.operator_service import build_operator_jwks_payload
from tigrbl_auth.services.tenant_discovery import (
    TENANT_JWKS_PATH,
    TENANT_OPENID_CONFIGURATION_PATH,
    build_tenant_openid_config,
    enabled_tenant_record,
)
from tigrbl_auth.services.jwks_service import build_jwks_document
from tigrbl_auth.standards.oidc.discovery_metadata import build_openid_config
from tigrbl_auth.standards.http.well_known import WELL_KNOWN_ENDPOINTS
from tigrbl_auth.standards.oauth2.rfc8414_metadata import ISSUER, JWKS_PATH
from tigrbl_auth.standards.oauth2.rfc9700 import discovery_policy_metadata

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


@discovery_api.route(TENANT_OPENID_CONFIGURATION_PATH, methods=["GET"], tags=[".well-known", "tenant"])
async def tenant_openid_configuration(request: Request, tenant_slug: str):
    deployment = deployment_from_request(request, settings)
    if not deployment.route_enabled(TENANT_OPENID_CONFIGURATION_PATH):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Tenant OIDC discovery disabled")
    if enabled_tenant_record(Path.cwd(), tenant_slug) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Tenant not found")
    return build_tenant_openid_config(deployment, tenant_slug)


@jwks_api.route(JWKS_PATH, methods=["GET"], tags=[".well-known"])
async def jwks(request: Request):
    deployment = deployment_from_request(request, settings)
    if not deployment.route_enabled(JWKS_PATH):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "JWKS publication disabled")
    return await build_jwks_document()


@jwks_api.route(TENANT_JWKS_PATH, methods=["GET"], tags=[".well-known", "tenant"])
async def tenant_jwks(request: Request, tenant_slug: str):
    deployment = deployment_from_request(request, settings)
    if not deployment.route_enabled(TENANT_JWKS_PATH):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Tenant JWKS publication disabled")
    if enabled_tenant_record(Path.cwd(), tenant_slug) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Tenant not found")
    return build_operator_jwks_payload(Path.cwd(), tenant=tenant_slug)


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
