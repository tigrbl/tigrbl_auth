"""OAuth/OIDC login and authorization-flow route composition."""

from __future__ import annotations

from tigrbl_identity_storage.framework import TigrblRouter

from tigrbl_identity_storage_runtime.authz_surface import router as authz_router
from tigrbl_identity_storage_runtime.login import router as login_router

router = TigrblRouter()
router.include_router(login_router)
router.include_router(authz_router)

__all__ = ["router"]
