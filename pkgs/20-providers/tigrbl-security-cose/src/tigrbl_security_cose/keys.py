"""Strict decoding and loading of COSE public keys."""

from __future__ import annotations

from collections.abc import Mapping

import cbor2
from cryptography.hazmat.primitives.asymmetric import ec, ed25519, rsa

MAX_COSE_KEY_BYTES = 8192


def decode_cose_key(encoded: bytes) -> Mapping[int, object]:
    if not isinstance(encoded, bytes) or not encoded:
        raise ValueError("encoded COSE key is required")
    if len(encoded) > MAX_COSE_KEY_BYTES:
        raise ValueError("encoded COSE key exceeds the supported size")
    value = cbor2.loads(encoded)
    if not isinstance(value, Mapping) or not all(isinstance(key, int) for key in value):
        raise ValueError("COSE key must be an integer-keyed CBOR map")
    if cbor2.dumps(dict(value), canonical=True) != encoded:
        raise ValueError("COSE key must use canonical CBOR encoding")
    if 1 not in value:
        raise ValueError("COSE key type is required")
    return dict(value)


def _bytes(value: object, name: str) -> bytes:
    if not isinstance(value, bytes) or not value:
        raise ValueError(f"COSE key {name} must be a non-empty byte string")
    return value


def load_cose_public_key(value: bytes | Mapping[int, object]):
    key = decode_cose_key(value) if isinstance(value, bytes) else dict(value)
    kty = key.get(1)
    if kty == 2:  # EC2
        curve_id = key.get(-1)
        curves = {1: ec.SECP256R1, 2: ec.SECP384R1, 3: ec.SECP521R1, 8: ec.SECP256K1}
        try:
            curve = curves[curve_id]()
        except KeyError as exc:
            raise ValueError(f"unsupported COSE EC2 curve: {curve_id}") from exc
        x = int.from_bytes(_bytes(key.get(-2), "x coordinate"), "big")
        y = int.from_bytes(_bytes(key.get(-3), "y coordinate"), "big")
        return ec.EllipticCurvePublicNumbers(x, y, curve).public_key()
    if kty == 3:  # RSA
        modulus = int.from_bytes(_bytes(key.get(-1), "RSA modulus"), "big")
        exponent = int.from_bytes(_bytes(key.get(-2), "RSA exponent"), "big")
        if modulus.bit_length() < 2048:
            raise ValueError("COSE RSA key must contain at least 2048 bits")
        return rsa.RSAPublicNumbers(exponent, modulus).public_key()
    if kty == 1:  # OKP
        if key.get(-1) != 6:
            raise ValueError(f"unsupported COSE OKP curve: {key.get(-1)}")
        return ed25519.Ed25519PublicKey.from_public_bytes(
            _bytes(key.get(-2), "OKP x coordinate")
        )
    raise ValueError(f"unsupported COSE key type: {kty}")


__all__ = ["MAX_COSE_KEY_BYTES", "decode_cose_key", "load_cose_public_key"]
