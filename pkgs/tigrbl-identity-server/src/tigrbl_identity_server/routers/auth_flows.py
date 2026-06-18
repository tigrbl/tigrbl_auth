from __future__ import annotations

"""Compatibility OAuth/OIDC flow router.

Canonical executable route implementations live under
``tigrbl_identity_server.rest.routers`` and protocol packages. This module only
composes those routers for older imports that expect one flow router.
"""

from tigrbl_identity_server.framework import TigrblRouter
from tigrbl_identity_server.rest.routers.login import api as login_api
from tigrbl_identity_server.routers.authz import api as authz_api

api = router = TigrblRouter()
api.include_router(login_api)
api.include_router(authz_api)

__all__ = ["api", "router"]
