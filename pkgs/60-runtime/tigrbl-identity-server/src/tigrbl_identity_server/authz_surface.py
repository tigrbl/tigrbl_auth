"""Legacy authorization and token route composition."""

from __future__ import annotations

from tigrbl import TigrblRouter

from tigrbl_identity_server.authorization_surface import router as authorize_router
from tigrbl_identity_server.token_surface import router as token_router

router = TigrblRouter()
router.include_router(authorize_router)
router.include_router(token_router)

__all__ = ["router"]
