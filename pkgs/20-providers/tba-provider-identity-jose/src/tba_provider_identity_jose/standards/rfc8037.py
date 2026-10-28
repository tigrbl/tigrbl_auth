"""Ed25519 signing and verification implemented with cryptography (RFC 8037)."""
from __future__ import annotations

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from ..configuration import settings

RFC8037_SPEC_URL = "https://www.rfc-editor.org/rfc/rfc8037"

def _private(key: bytes | Ed25519PrivateKey) -> Ed25519PrivateKey:
    if isinstance(key, Ed25519PrivateKey): return key
    if bytes(key).startswith(b"-----BEGIN"):
        loaded = serialization.load_pem_private_key(bytes(key), password=None)
        if isinstance(loaded, Ed25519PrivateKey): return loaded
    return Ed25519PrivateKey.from_private_bytes(bytes(key)[:32])

def _public(key: bytes | Ed25519PublicKey) -> Ed25519PublicKey:
    if isinstance(key, Ed25519PublicKey): return key
    if bytes(key).startswith(b"-----BEGIN"):
        loaded = serialization.load_pem_public_key(bytes(key))
        if isinstance(loaded, Ed25519PublicKey): return loaded
    return Ed25519PublicKey.from_public_bytes(bytes(key))

def sign_eddsa(message: bytes, key: bytes | Ed25519PrivateKey, *, enabled: bool | None = None) -> bytes:
    if enabled is None: enabled = settings.enable_rfc8037
    return _private(key).sign(message) if enabled else message

def verify_eddsa(message: bytes, signature: bytes, key: bytes | Ed25519PublicKey, *, enabled: bool | None = None) -> bool:
    if enabled is None: enabled = settings.enable_rfc8037
    if not enabled: return True
    try: _public(key).verify(signature, message); return True
    except Exception: return False

__all__ = ["RFC8037_SPEC_URL", "sign_eddsa", "verify_eddsa"]
