"""Compatibility facade for `tba_protocol_oidc.tenant_discovery`."""

from tba_auth._split_imports import alias_module as _alias_module

_module = _alias_module(
    __name__,
    "tba_protocol_oidc.tenant_discovery",
    "tba-protocol-oidc",
)
globals().update(_module.__dict__)
