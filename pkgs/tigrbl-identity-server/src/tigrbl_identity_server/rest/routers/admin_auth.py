"""Compatibility bridge for storage-owned admin authentication routes."""

from __future__ import annotations

from warnings import warn

warn(
    "tigrbl_identity_server.rest.routers.admin_auth is deprecated; "
    "import tigrbl_identity_storage.tables.user instead.",
    DeprecationWarning,
    stacklevel=2,
)

from tigrbl_identity_storage.tables.user import (
    admin_api as api,
    admin_change_password,
    admin_forgot_password,
    admin_login,
    admin_login_browser_redirect,
    admin_logout,
    admin_reset_password,
    admin_router as router,
    admin_session,
)

__all__ = [
    "api",
    "admin_change_password",
    "admin_forgot_password",
    "admin_login",
    "admin_login_browser_redirect",
    "admin_logout",
    "admin_reset_password",
    "admin_session",
    "router",
]
