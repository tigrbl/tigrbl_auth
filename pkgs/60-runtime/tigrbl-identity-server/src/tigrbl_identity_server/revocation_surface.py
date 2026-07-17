"""Runtime composition for the RFC 7009 HTTP carrier."""

from __future__ import annotations

from tigrbl import Request, TigrblApp
from tigrbl_auth_router_oauth_revocation import (
    build_revocation_router,
    include_revocation_endpoint as include_http_revocation_endpoint,
)
from tigrbl_identity_runtime.settings import settings

from .security.token_revocation import build_rfc7009_revocation_service


def _service_for_request(request: Request):
    return build_rfc7009_revocation_service(settings)


router = build_revocation_router(service_for_request=_service_for_request)


def include_revocation_endpoint(app: TigrblApp) -> None:
    include_http_revocation_endpoint(
        app,
        router,
        enabled=bool(settings.enable_rfc7009),
    )


include_rfc7009 = include_revocation_endpoint


__all__ = [
    "include_revocation_endpoint",
    "include_rfc7009",
    "router",
]
