from __future__ import annotations

"""Compatibility bridge for ClientRegistration-owned registration routes."""

from warnings import warn

warn(
    "tigrbl_identity_server.rest.routers.register is deprecated; "
    "import tigrbl_identity_storage.tables.client_registration instead.",
    DeprecationWarning,
    stacklevel=2,
)

from tigrbl_identity_storage.tables.client_registration import (
    _sync_client_registration,
    api,
    register,
    register_delete,
    register_get,
    register_put,
    router,
)

__all__ = [
    "api",
    "router",
    "register",
    "_sync_client_registration",
    "register_delete",
    "register_get",
    "register_put",
]
