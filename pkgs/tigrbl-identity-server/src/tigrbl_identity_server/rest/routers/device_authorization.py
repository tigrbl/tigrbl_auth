from __future__ import annotations

"""Compatibility bridge for DeviceCode-owned device authorization route."""

from warnings import warn

warn(
    "tigrbl_identity_server.rest.routers.device_authorization is deprecated; "
    "import tigrbl_identity_storage.tables.device_code instead.",
    DeprecationWarning,
    stacklevel=2,
)

from tigrbl_identity_storage.tables.device_code import api, device_authorization, router

__all__ = ["api", "router", "device_authorization"]
