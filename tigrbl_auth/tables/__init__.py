"""Compatibility facade for canonical identity storage tables.

The authoritative implementations live in ``tigrbl_identity_storage.tables``.
"""

from importlib import import_module
import sys

from tigrbl_auth._identity_storage import ensure_identity_storage_importable

ensure_identity_storage_importable()

_LEGACY_NAME = __name__
_SUBMODULES = (
    "api_key",
    "audit_event",
    "auth_code",
    "auth_session",
    "client",
    "client_registration",
    "consent",
    "delegation_grant",
    "device_code",
    "engine",
    "key_rotation_event",
    "logout_state",
    "pushed_authorization_request",
    "realm",
    "revoked_token",
    "service",
    "service_key",
    "tenant",
    "token_record",
    "user",
)

import tigrbl_identity_storage.tables as _module

for _submodule in _SUBMODULES:
    sys.modules[f"{_LEGACY_NAME}.{_submodule}"] = import_module(
        f"tigrbl_identity_storage.tables.{_submodule}"
    )

sys.modules[__name__] = _module
globals().update(_module.__dict__)
