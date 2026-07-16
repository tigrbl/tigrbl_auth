"""Compatibility facade for principal-authentication credential lifecycle."""

from tigrbl_principal_authentication import lifecycle as _lifecycle

globals().update(
    {name: value for name, value in vars(_lifecycle).items() if not name.startswith("__")}
)

__all__ = [name for name in vars(_lifecycle) if not name.startswith("_")]
