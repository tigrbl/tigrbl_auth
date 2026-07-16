"""Compatibility facade for principal-authentication proof bindings."""

from tigrbl_principal_authentication import proof_bindings as _proof_bindings

globals().update(
    {
        name: value
        for name, value in vars(_proof_bindings).items()
        if not name.startswith("__")
    }
)

__all__ = [name for name in vars(_proof_bindings) if not name.startswith("_")]
