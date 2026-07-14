"""Compatibility facade for the layer-60 UserInfo runtime."""

from __future__ import annotations

from tigrbl_auth._split_imports import alias_module as _alias_module

_module = _alias_module(
    __name__,
    "tigrbl_identity_server.userinfo_runtime",
    "tigrbl-identity-server",
)

globals().update(_module.__dict__)
