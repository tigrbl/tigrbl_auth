"""Compatibility facade for split COSE key ownership."""

from tigrbl_cose_concrete.keys import decode_cose_key
from tigrbl_cose_cryptography_provider.keys import load_cose_public_key

__all__ = ["decode_cose_key", "load_cose_public_key"]
