"""OAuth/OIDC login and authorization-flow route composition."""

from __future__ import annotations

from tigrbl import TigrblRouter

from .authz_surface import router as authz_router
from .introspection_surface import router as introspection_router
from .login_surface import router as login_router

router = TigrblRouter()
router.include_router(login_router)
router.include_router(authz_router)
router.include_router(introspection_router)

__all__ = ["router"]
