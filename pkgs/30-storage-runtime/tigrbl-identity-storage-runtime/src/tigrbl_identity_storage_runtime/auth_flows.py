"""OAuth/OIDC login and authorization-flow route composition."""

from __future__ import annotations

from tigrbl_identity_storage.framework import TigrblRouter

from tigrbl_identity_storage.tables.auth_session import login_api
from tigrbl_identity_storage_runtime.authz_surface import router as authz_router

router = TigrblRouter()
router.include_router(login_api)
router.include_router(authz_router)

__all__ = ["router"]
