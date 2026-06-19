"""Storage-owned my-account route composition."""

from __future__ import annotations

from tigrbl_identity_storage.framework import TigrblRouter

from ..auth_session import account_api as session_account_api
from ..consent import account_api as consent_account_api
from ._table import account_api as user_account_api

api = router = TigrblRouter()
api.include_router(user_account_api)
api.include_router(session_account_api)
api.include_router(consent_account_api)

__all__ = ["api", "router"]
