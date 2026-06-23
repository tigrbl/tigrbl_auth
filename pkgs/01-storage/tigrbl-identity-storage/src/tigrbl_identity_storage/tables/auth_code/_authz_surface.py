"""Storage-owned authz route composition."""

from __future__ import annotations

from tigrbl_identity_storage.framework import TigrblRouter

from . import api as authorize_api
from tigrbl_identity_storage_runtime.introspection import api as introspection_api
from ..token_record import api as token_api

api = router = TigrblRouter()
api.include_router(authorize_api)
api.include_router(token_api)
api.include_router(introspection_api)

__all__ = ["api", "router"]
