"""Compatibility facade for the cryptography-backed COSE provider."""

from tigrbl_cose_cryptography_provider.signatures import verify_detached_signature

__all__ = ["verify_detached_signature"]
