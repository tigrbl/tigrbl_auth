"""Cryptography-backed COSE provider."""

from .keys import load_cose_public_key
from .signatures import verify_detached_signature

__all__ = ["load_cose_public_key", "verify_detached_signature"]
