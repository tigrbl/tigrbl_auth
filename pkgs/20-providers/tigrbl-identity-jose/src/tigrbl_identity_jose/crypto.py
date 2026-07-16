"""Compatibility facade for tigrbl-jose-swarmauri-provider."""

from tigrbl_jose_swarmauri_provider import crypto as _provider_crypto
from tigrbl_secret_hashing_bcrypt_provider import hash_pw, verify_pw

globals().update(
    {
        name: value
        for name, value in vars(_provider_crypto).items()
        if not name.startswith("__")
    }
)

__all__ = [*_provider_crypto.__all__, "hash_pw", "verify_pw"]
