from __future__ import annotations

"""Compatibility bridge for PushedAuthorizationRequest-owned PAR route."""

from warnings import warn

warn(
    "tigrbl_identity_server.rest.routers.par is deprecated; "
    "import tigrbl_identity_storage.tables.pushed_authorization_request instead.",
    DeprecationWarning,
    stacklevel=2,
)

from tigrbl_identity_storage.tables.pushed_authorization_request import api, par, router

__all__ = ["api", "router", "par"]
