"""RFC 7517 - JSON Web Key (JWK) utilities.

The canonical implementation prefers the runtime key-management service, but a
small dependency-light Ed25519 fallback is preserved for checkpoint testing and
standalone helper use.
"""

from __future__ import annotations

import asyncio
import base64
import hashlib
from functools import lru_cache
from typing import Final

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, NoEncryption, PrivateFormat, PublicFormat

from tigrbl_auth.config.settings import settings

try:  # pragma: no cover - exercised when the full runtime stack is installed
    from tigrbl_auth.services.key_management import _load_keypair, _provider
except Exception:  # pragma: no cover - dependency-light checkpoint fallback
    _load_keypair = None
    _provider = None

RFC7517_SPEC_URL: Final = "https://www.rfc-editor.org/rfc/rfc7517"


def _b64u(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode("ascii")


@lru_cache(maxsize=1)
def _fallback_keypair() -> tuple[bytes, bytes, str]:
    private_key = Ed25519PrivateKey.generate()
    private_bytes = private_key.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())
    public_bytes = private_key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
    kid = f"fallback-ed25519:{hashlib.sha256(public_bytes).hexdigest()[:24]}"
    return private_bytes, public_bytes, kid


def load_signing_jwk() -> dict:
    """Return the private signing key as a JWK mapping."""
    if not settings.enable_rfc7517:
        raise RuntimeError(f"RFC 7517 support disabled: {RFC7517_SPEC_URL}")
    if _load_keypair is not None and _provider is not None:
        try:
            kid, priv, pub = _load_keypair()
            kp = _provider()
            ref = asyncio.run(kp.get_key(kid, include_secret=True))
            sk = ref.material or priv
            pk = ref.public or pub
            d = sk[:32] if len(sk) > 32 else sk
            return {"kty": "OKP", "crv": "Ed25519", "kid": kid, "d": _b64u(d), "x": _b64u(pk)}
        except Exception:
            pass
    private_bytes, public_bytes, kid = _fallback_keypair()
    return {"kty": "OKP", "crv": "Ed25519", "kid": kid, "d": _b64u(private_bytes), "x": _b64u(public_bytes)}


def load_public_jwk() -> dict:
    """Return the public key as a JWK mapping."""
    if not settings.enable_rfc7517:
        raise RuntimeError(f"RFC 7517 support disabled: {RFC7517_SPEC_URL}")
    if _load_keypair is not None and _provider is not None:
        try:
            kid, _, _ = _load_keypair()
            kp = _provider()
            jwk = asyncio.run(kp.get_public_jwk(kid))
            if isinstance(jwk, dict):
                jwk.setdefault("kid", kid)
                return jwk
            return {"kty": "OKP", "crv": "Ed25519", "kid": kid}
        except Exception:
            pass
    _, public_bytes, kid = _fallback_keypair()
    return {"kty": "OKP", "crv": "Ed25519", "kid": kid, "x": _b64u(public_bytes)}


__all__ = ["load_signing_jwk", "load_public_jwk", "RFC7517_SPEC_URL"]
