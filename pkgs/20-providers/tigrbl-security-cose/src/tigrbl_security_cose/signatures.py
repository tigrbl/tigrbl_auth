"""Detached signature verification using COSE public-key metadata."""

from __future__ import annotations

from collections.abc import Mapping

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, ed25519, padding, rsa

from .algorithms import resolve_cose_algorithm
from .keys import load_cose_public_key


def _hash(name: str | None) -> hashes.HashAlgorithm:
    algorithms = {
        "sha256": hashes.SHA256,
        "sha384": hashes.SHA384,
        "sha512": hashes.SHA512,
    }
    try:
        return algorithms[name]()
    except KeyError as exc:
        raise ValueError(f"unsupported signature hash: {name}") from exc


def verify_detached_signature(
    *,
    public_key: bytes | Mapping[int, object],
    algorithm: int,
    message: bytes,
    signature: bytes,
) -> bool:
    if not message or not signature:
        raise ValueError(
            "detached signature verification requires message and signature"
        )
    specification = resolve_cose_algorithm(algorithm)
    key = load_cose_public_key(public_key)
    try:
        if specification.key_type == "EC2" and isinstance(
            key, ec.EllipticCurvePublicKey
        ):
            key.verify(signature, message, ec.ECDSA(_hash(specification.hash_name)))
        elif specification.name == "EdDSA" and isinstance(
            key, ed25519.Ed25519PublicKey
        ):
            key.verify(signature, message)
        elif specification.key_type == "RSA" and isinstance(key, rsa.RSAPublicKey):
            scheme = (
                padding.PSS(
                    mgf=padding.MGF1(_hash(specification.hash_name)),
                    salt_length=padding.PSS.DIGEST_LENGTH,
                )
                if specification.name.startswith("PS")
                else padding.PKCS1v15()
            )
            key.verify(signature, message, scheme, _hash(specification.hash_name))
        else:
            raise ValueError("COSE key type does not match the requested algorithm")
    except InvalidSignature:
        return False
    return True


__all__ = ["verify_detached_signature"]
