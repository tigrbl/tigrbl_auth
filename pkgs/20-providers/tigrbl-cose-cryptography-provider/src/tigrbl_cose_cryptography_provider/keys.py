"""Translate COSE key values into cryptography public keys."""

from collections.abc import Mapping

from cryptography.hazmat.primitives.asymmetric import ec, ed25519, rsa
from tigrbl_cose_concrete import decode_cose_key


def _bytes(value: object, name: str) -> bytes:
    if not isinstance(value, bytes) or not value:
        raise ValueError(f"COSE key {name} must be non-empty bytes")
    return value


def load_cose_public_key(value: bytes | Mapping[int, object]):
    key = decode_cose_key(value) if isinstance(value, bytes) else value
    key_type = key.get(1)
    if key_type == 1:
        curve = key.get(-1)
        if curve != 6:
            raise ValueError(f"unsupported OKP curve: {curve!r}")
        return ed25519.Ed25519PublicKey.from_public_bytes(_bytes(key.get(-2), "x"))
    if key_type == 2:
        curve_id = key.get(-1)
        curves = {1: ec.SECP256R1(), 2: ec.SECP384R1(), 3: ec.SECP521R1()}
        if curve_id not in curves:
            raise ValueError(f"unsupported EC2 curve: {curve_id!r}")
        numbers = ec.EllipticCurvePublicNumbers(
            int.from_bytes(_bytes(key.get(-2), "x"), "big"),
            int.from_bytes(_bytes(key.get(-3), "y"), "big"),
            curves[curve_id],
        )
        return numbers.public_key()
    if key_type == 3:
        return rsa.RSAPublicNumbers(
            int.from_bytes(_bytes(key.get(-2), "e"), "big"),
            int.from_bytes(_bytes(key.get(-1), "n"), "big"),
        ).public_key()
    raise ValueError(f"unsupported COSE key type: {key_type!r}")
