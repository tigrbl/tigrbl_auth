"""My-account route composition for storage runtime."""

from __future__ import annotations

from tigrbl_identity_storage.framework import TigrblRouter

from tigrbl_identity_storage.tables.auth_session import account_api as session_account_api
from tigrbl_identity_storage.tables.user import account_api as user_account_api
from .account_consent import api as consent_account_api

api = router = TigrblRouter()
api.include_router(user_account_api)
api.include_router(session_account_api)
api.include_router(consent_account_api)

__all__ = ["api", "router"]
