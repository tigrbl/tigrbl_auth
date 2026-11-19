"""X448 direct key agreement and RFC 7518 Concat KDF for compact JWE."""

from collections.abc import Mapping

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.x448 import X448PublicKey
from cryptography.hazmat.primitives.kdf.concatkdf import ConcatKDFHash
from tba_primitives_identity.base64url import base64url_decode, base64url_encode


def _decode_base64url(value: object) -> bytes:
    if not isinstance(value, str):
        raise ValueError("expected an unpadded base64url string")
    raw = base64url_decode(value)
    if base64url_encode(raw) != value:
        raise ValueError("expected an unpadded base64url string")
    return raw


def public_jwk(public_key: X448PublicKey) -> dict[str, str]:
    return {
        "kty": "OKP",
        "crv": "X448",
        "x": base64url_encode(public_key.public_bytes_raw()),
    }


def load_public_jwk(value: object) -> X448PublicKey:
    if (
        not isinstance(value, Mapping)
        or (value.get("kty"), value.get("crv")) != ("OKP", "X448")
        or "d" in value
    ):
        raise ValueError("epk must be a public OKP/X448 JWK")
    return X448PublicKey.from_public_bytes(_decode_base64url(value.get("x")))


def _field(value: bytes) -> bytes:
    return len(value).to_bytes(4, "big") + value


def _concat_kdf(
    secret: bytes, enc: str, key_length: int, apu: bytes = b"", apv: bytes = b""
) -> bytes:
    other_info = (
        _field(enc.encode("ascii"))
        + _field(apu)
        + _field(apv)
        + (key_length * 8).to_bytes(4, "big")
    )
    return ConcatKDFHash(
        algorithm=hashes.SHA256(), length=key_length, otherinfo=other_info
    ).derive(secret)


def content_key(secret: bytes, headers: Mapping[str, object]) -> bytes:
    apu = _decode_base64url(headers["apu"]) if "apu" in headers else b""
    apv = _decode_base64url(headers["apv"]) if "apv" in headers else b""
    if "apu" in headers and "apv" in headers and apu == apv:
        raise ValueError("apu and apv must be distinct")
    return _concat_kdf(secret, "A256GCM", 32, apu, apv)
