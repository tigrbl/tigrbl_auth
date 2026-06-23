"""OAuth/OIDC login and authorization-flow route composition."""

from __future__ import annotations

from tigrbl_identity_storage.framework import TigrblRouter

from tigrbl_identity_storage.tables.auth_session import login_api
from tigrbl_identity_storage_runtime.authz_surface import api as authz_api

api = router = TigrblRouter()
api.include_router(login_api)
api.include_router(authz_api)

__all__ = ["api", "router"]
