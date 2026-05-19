"""RFC 7515 - JSON Web Signature (JWS) helpers.

The canonical implementation prefers the Swarmauri signer, but it also exposes
an internal dependency-light compact JWS fallback so helper tests and governance
workflows can run without the full Tigrbl runtime stack.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
from typing import Any, Final, Mapping

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

try:  # pragma: no cover - exercised when the full runtime stack is installed
    from tigrbl_auth.framework import JWAAlg, JwsSignerVerifier
except Exception:  # pragma: no cover - dependency-light checkpoint fallback
    JWAAlg = None
    JwsSignerVerifier = None

from tigrbl_auth.config.settings import settings

RFC7515_SPEC_URL: Final = "https://www.rfc-editor.org/rfc/rfc7515"
_signer = JwsSignerVerifier() if JwsSignerVerifier is not None else None


def _b64u_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64u_decode(text: str) -> bytes:
    padding = "=" * (-len(text) % 4)
    return base64.urlsafe_b64decode((text + padding).encode("ascii"))


def _oct_key_bytes(key: Mapping[str, Any]) -> bytes:
    raw = key.get("key")
    if isinstance(raw, (bytes, bytearray)):
        return bytes(raw)
    material = key.get("k")
    if isinstance(material, str):
        return _b64u_decode(material)
    if isinstance(material, (bytes, bytearray)):
        return bytes(material)
    raise RuntimeError("missing symmetric oct key material for dependency-light JWS fallback")


def _ed25519_private_key(key: Mapping[str, Any]) -> Ed25519PrivateKey:
    raw = key.get("key")
    if isinstance(raw, (bytes, bytearray)):
        material = bytes(raw)
        if material.startswith(b"-----BEGIN"):
            loaded = serialization.load_pem_private_key(material, password=None)
            if isinstance(loaded, Ed25519PrivateKey):
                return loaded
        if len(material) >= 32:
            return Ed25519PrivateKey.from_private_bytes(material[:32])
    material = key.get("d")
    if isinstance(material, str):
        decoded = _b64u_decode(material)
        if len(decoded) >= 32:
            return Ed25519PrivateKey.from_private_bytes(decoded[:32])
    raise RuntimeError("missing Ed25519 private key material for dependency-light JWS fallback")


def _ed25519_public_key(key: Mapping[str, Any]) -> Ed25519PublicKey:
    raw = key.get("public") or key.get("key")
    if isinstance(raw, (bytes, bytearray)):
        material = bytes(raw)
        if material.startswith(b"-----BEGIN"):
            loaded = serialization.load_pem_public_key(material)
            if isinstance(loaded, Ed25519PublicKey):
                return loaded
        if len(material) == 32:
            return Ed25519PublicKey.from_public_bytes(material)
    material = key.get("x")
    if isinstance(material, str):
        decoded = _b64u_decode(material)
        if len(decoded) == 32:
            return Ed25519PublicKey.from_public_bytes(decoded)
    raise RuntimeError("missing Ed25519 public key material for dependency-light JWS fallback")


def _fallback_algorithm_for_key(key: Mapping[str, Any]) -> str:
    kty = str(key.get("kty") or "").lower()
    if kty == "oct":
        return "HS256"
    if kty in {"okp", "eddsa"} or str(key.get("alg") or "").upper() == "EDDSA":
        return "EdDSA"
    raise RuntimeError("dependency-light JWS fallback only supports oct/HS256 and OKP/EdDSA keys")


def _fallback_sign(payload: str, key: Mapping[str, Any]) -> str:
    alg = _fallback_algorithm_for_key(key)
    header = {"alg": alg, "typ": "JWT"}
    header_segment = _b64u_encode(json.dumps(header, separators=(",", ":")).encode())
    payload_segment = _b64u_encode(payload.encode())
    signing_input = f"{header_segment}.{payload_segment}".encode("ascii")
    if alg == "HS256":
        sig = hmac.new(_oct_key_bytes(key), signing_input, hashlib.sha256).digest()
    else:
        sig = _ed25519_private_key(key).sign(signing_input)
    return f"{signing_input.decode('ascii')}.{_b64u_encode(sig)}"


def _fallback_verify(token: str, key: Mapping[str, Any]) -> str:
    try:
        header_segment, payload_segment, sig_segment = token.split(".")
    except ValueError as exc:
        raise RuntimeError("invalid compact JWS serialization") from exc
    signing_input = f"{header_segment}.{payload_segment}".encode("ascii")
    header = json.loads(_b64u_decode(header_segment).decode("utf-8"))
    alg = str(header.get("alg") or "")
    signature = _b64u_decode(sig_segment)
    if alg == "HS256":
        expected = hmac.new(_oct_key_bytes(key), signing_input, hashlib.sha256).digest()
        if not hmac.compare_digest(expected, signature):
            raise RuntimeError("invalid JWS signature")
    elif alg == "EdDSA":
        _ed25519_public_key(key).verify(signature, signing_input)
    else:
        raise RuntimeError(f"unsupported dependency-light JWS alg: {alg}")
    return _b64u_decode(payload_segment).decode("utf-8")


async def sign_jws(payload: str, key: Mapping[str, Any]) -> str:
    """Return a JWS compact serialization of *payload* using *key*."""
    if not settings.enable_rfc7515:
        raise RuntimeError(f"RFC 7515 support disabled: {RFC7515_SPEC_URL}")
    if _signer is not None and JWAAlg is not None:
        alg = JWAAlg.HS256 if key.get("kty") == "oct" else JWAAlg.EDDSA
        return await _signer.sign_compact(payload=payload, alg=alg, key=key)
    return _fallback_sign(payload, key)


async def verify_jws(token: str, key: Mapping[str, Any]) -> str:
    """Verify *token* and return the decoded payload as a string."""
    if not settings.enable_rfc7515:
        raise RuntimeError(f"RFC 7515 support disabled: {RFC7515_SPEC_URL}")
    if _signer is not None:
        result = await _signer.verify_compact(token, jwks_resolver=lambda _k, _a: key)
        return result.payload.decode()
    return _fallback_verify(token, key)


__all__ = ["sign_jws", "verify_jws", "RFC7515_SPEC_URL"]
