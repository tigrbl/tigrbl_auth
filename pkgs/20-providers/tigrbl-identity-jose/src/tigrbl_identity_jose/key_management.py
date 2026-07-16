"""Compatibility facade for tigrbl-jose-swarmauri-provider."""

from tigrbl_jose_swarmauri_provider import key_management as _provider_module
from tigrbl_secret_hashing_bcrypt_provider import hash_pw, verify_pw

globals().update(
    {
        name: value
        for name, value in vars(_provider_module).items()
        if not name.startswith("__")
    }
)

__all__ = [
    *_provider_module.__all__,
    "hash_pw",
    "verify_pw",
]
