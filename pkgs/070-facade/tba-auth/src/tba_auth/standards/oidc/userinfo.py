"""Compatibility facade for the layer-60 UserInfo runtime."""

from __future__ import annotations

from tba_auth._split_imports import alias_module as _alias_module

_module = _alias_module(
    __name__,
    "tba_server_identity.userinfo_runtime",
    "tba-server-identity",
)

globals().update(_module.__dict__)
