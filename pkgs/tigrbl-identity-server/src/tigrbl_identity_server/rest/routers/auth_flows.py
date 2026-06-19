from __future__ import annotations

"""Compatibility bridge for AuthSession-owned auth-flow routes."""

from warnings import warn

warn(
    "tigrbl_identity_server.rest.routers.auth_flows is deprecated; "
    "import tigrbl_identity_storage.tables.auth_session instead.",
    DeprecationWarning,
    stacklevel=2,
)

from tigrbl_identity_storage.tables.auth_session import (
    login,
    login_api as api,
    login_router as router,
)

__all__ = ["api", "router", "login"]
