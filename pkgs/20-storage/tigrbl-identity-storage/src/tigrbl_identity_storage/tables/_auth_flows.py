"""Storage-owned OAuth/OIDC flow route composition."""

from __future__ import annotations

from tigrbl_identity_server.framework import TigrblRouter

from ._authz_routes import api as authz_api
from .auth_session import login_api

api = router = TigrblRouter()
api.include_router(login_api)
api.include_router(authz_api)

__all__ = ["api", "router"]
