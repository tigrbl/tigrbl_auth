"""Cryptography-backed verification of detached COSE signatures."""

from collections.abc import Mapping

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, ed25519, padding, rsa
from tigrbl_cose_concrete import resolve_cose_algorithm

from .keys import load_cose_public_key


def _hash(name: str | None) -> hashes.HashAlgorithm:
    values = {"sha256": hashes.SHA256, "sha384": hashes.SHA384, "sha512": hashes.SHA512}
    if name not in values:
        raise ValueError(f"unsupported COSE hash: {name!r}")
    return values[name]()


def verify_detached_signature(
    *,
    algorithm: int,
    public_key: bytes | Mapping[int, object],
    signing_input: bytes | None = None,
    message: bytes | None = None,
    signature: bytes,
) -> bool:
    if (signing_input is None) == (message is None):
        raise ValueError("provide exactly one of signing_input or message")
    signed_bytes = signing_input if signing_input is not None else message
    assert signed_bytes is not None
    descriptor = resolve_cose_algorithm(algorithm)
    key = load_cose_public_key(public_key)
    try:
        if isinstance(key, ed25519.Ed25519PublicKey):
            key.verify(signature, signed_bytes)
        elif isinstance(key, ec.EllipticCurvePublicKey):
            key.verify(signature, signed_bytes, ec.ECDSA(_hash(descriptor.hash_name)))
        elif isinstance(key, rsa.RSAPublicKey):
            hash_algorithm = _hash(descriptor.hash_name)
            rsa_padding = (
                padding.PSS(
                    mgf=padding.MGF1(hash_algorithm),
                    salt_length=hash_algorithm.digest_size,
                )
                if descriptor.name.startswith("PS")
                else padding.PKCS1v15()
            )
            key.verify(signature, signed_bytes, rsa_padding, hash_algorithm)
        else:
            raise ValueError("unsupported COSE public key implementation")
    except InvalidSignature:
        return False
    return True
