from __future__ import annotations

"""Compatibility bridge for table-owned my-account routes."""

from warnings import warn

warn(
    "tigrbl_identity_server.rest.routers.my_account is deprecated; import "
    "tigrbl_identity_storage.tables.user, "
    "tigrbl_identity_storage.tables.auth_session, and "
    "tigrbl_identity_storage.tables.consent instead.",
    DeprecationWarning,
    stacklevel=2,
)

from tigrbl_identity_server.framework import TigrblRouter
from tigrbl_identity_storage.tables.auth_session import account_api as session_account_api
from tigrbl_identity_storage.tables.consent import account_api as consent_account_api
from tigrbl_identity_storage.tables.user import (
    account_api as user_account_api,
    change_account_password,
    get_account_profile,
    update_account_profile,
)
from tigrbl_identity_storage.tables.auth_session import (
    list_account_sessions,
    revoke_account_session,
)
from tigrbl_identity_storage.tables.consent import (
    list_account_authorized_apps,
    list_account_consents,
    revoke_account_authorized_app,
    revoke_account_consent,
)

api = router = TigrblRouter()
api.include_router(user_account_api)
api.include_router(session_account_api)
api.include_router(consent_account_api)

__all__ = [
    "api",
    "router",
    "change_account_password",
    "get_account_profile",
    "list_account_authorized_apps",
    "list_account_consents",
    "list_account_sessions",
    "revoke_account_authorized_app",
    "revoke_account_consent",
    "revoke_account_session",
    "update_account_profile",
]
