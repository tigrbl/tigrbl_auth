"""Authorization Server Metadata support (RFC 8414)."""

from __future__ import annotations

from typing import Final

from tigrbl_identity_storage.framework import HTTPException, Request, TigrblApp, TigrblRouter, status
from tigrbl_identity_runtime.deployment import deployment_from_app, deployment_from_request
from tigrbl_identity_runtime.settings import settings
from ._oidc_discovery import refresh_discovery_cache
from tigrbl_auth_protocol_oidc.standards.discovery_metadata import build_openid_config

RFC8414_SPEC_URL: Final = "https://www.rfc-editor.org/rfc/rfc8414"

api = TigrblRouter()
router = api


@api.route("/.well-known/oauth-authorization-server", methods=["GET"], include_in_schema=True, tags=[".well-known"])
async def authorization_server_metadata(request: Request):
    if not settings.enable_rfc8414:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"RFC 8414 disabled: {RFC8414_SPEC_URL}")
    deployment = deployment_from_request(request, settings)
    if not deployment.route_enabled("/.well-known/oauth-authorization-server"):
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"RFC 8414 disabled: {RFC8414_SPEC_URL}")
    return build_openid_config(deployment)


def include_rfc8414(app: TigrblApp) -> None:
    path = "/.well-known/oauth-authorization-server"
    deployment = deployment_from_app(app, settings)
    if deployment.route_enabled(path) and not any((getattr(route, 'path', None) or getattr(route, 'path_template', None)) == path for route in app.router.routes):
        app.include_router(api)


__all__ = ["api", "router", "include_rfc8414", "RFC8414_SPEC_URL", "refresh_discovery_cache"]
