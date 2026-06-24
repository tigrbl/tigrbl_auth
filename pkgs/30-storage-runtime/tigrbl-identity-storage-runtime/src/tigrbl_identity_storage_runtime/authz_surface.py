"""OAuth authorization/token/introspection route composition."""

from __future__ import annotations

from tigrbl_identity_storage.framework import TigrblRouter

from tigrbl_identity_storage_runtime.authorization import router as authorize_router
from tigrbl_identity_storage_runtime.introspection import api as introspection_api
from tigrbl_identity_storage.tables.token_record import api as token_api

router = TigrblRouter()
router.include_router(authorize_router)
router.include_router(token_api)
router.include_router(introspection_api)

__all__ = ["router"]
