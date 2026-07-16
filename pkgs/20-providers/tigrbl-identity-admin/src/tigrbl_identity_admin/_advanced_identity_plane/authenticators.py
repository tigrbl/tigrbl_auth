"""Compatibility facade for tigrbl-advanced-authentication-capability."""

from tigrbl_advanced_authentication_capability import authenticators as _authenticators

globals().update(
    {
        name: value
        for name, value in vars(_authenticators).items()
        if not name.startswith("__")
    }
)

__all__ = [name for name in vars(_authenticators) if not name.startswith("_")]
