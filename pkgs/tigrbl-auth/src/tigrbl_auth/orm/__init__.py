"""Compatibility facade for `tigrbl_identity_storage.orm`."""

from tigrbl_auth._split_imports import alias_module as _alias_module

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

_LEGACY_NAME = __name__
_module = _alias_module(__name__, "tigrbl_identity_storage.orm", "tigrbl-identity-storage")
globals().update(_module.__dict__)

for _submodule in _SUBMODULES:
    _alias_module(
        f"{_LEGACY_NAME}.{_submodule}",
        f"tigrbl_identity_storage.orm.{_submodule}",
        "tigrbl-identity-storage",
    )
