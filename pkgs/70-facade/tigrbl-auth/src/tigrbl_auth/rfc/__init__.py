"""Compatibility aliases for legacy RFC helper import paths."""

from __future__ import annotations

from tigrbl_auth._split_imports import alias_module as _alias_module


_LEGACY_NAME = __name__

_OAUTH_RFC_MODULES = (
    "rfc6749",
    "rfc6749_token",
    "rfc6750",
    "rfc7009",
    "rfc7521",
    "rfc7523",
    "rfc7519",
    "rfc7591",
    "rfc7592",
    "rfc7636_pkce",
    "rfc7662",
    "rfc7662_introspection",
    "rfc8252",
    "rfc8414",
    "rfc8414_metadata",
    "rfc8523",
    "rfc8628",
    "rfc8693",
    "rfc8705",
    "rfc8707",
    "rfc8725",
    "rfc9068",
    "rfc9101",
    "rfc9126",
    "rfc9207",
    "rfc9396",
    "rfc9449_dpop",
)
_JOSE_RFC_MODULES = (
    "rfc7515",
    "rfc7516",
    "rfc7517",
    "rfc7518",
    "rfc7520",
    "rfc7638",
    "rfc7800",
    "rfc8037",
    "rfc8176",
    "rfc8812",
)
_CORE_RFC_MODULES = ("rfc8785",)

for _name in _OAUTH_RFC_MODULES:
    _alias_module(
        f"{_LEGACY_NAME}.{_name}",
        f"tigrbl_auth_protocol_oauth.standards.{_name}",
        "tigrbl-auth-protocol-oauth",
    )

for _name in _JOSE_RFC_MODULES:
    _alias_module(
        f"{_LEGACY_NAME}.{_name}",
        f"tigrbl_identity_jose.standards.{_name}",
        "tigrbl-identity-jose",
    )

__all__ = sorted((*_OAUTH_RFC_MODULES, *_JOSE_RFC_MODULES, *_CORE_RFC_MODULES))
