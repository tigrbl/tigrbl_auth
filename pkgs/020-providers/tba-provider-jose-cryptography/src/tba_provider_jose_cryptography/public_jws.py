"""Verify compact JWS with an explicitly selected asymmetric public JWK."""

from collections.abc import Mapping

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import (
    ec,
    ed25519,
    ed448,
    padding,
    rsa,
    utils,
)
from tba_concrete_jws import parse_jws_compact
from tba_primitives_identity import base64url_decode, base64url_encode

_EC = {"ES256": ec.SECP256R1, "ES384": ec.SECP384R1, "ES512": ec.SECP521R1}
_HASH = {"256": hashes.SHA256, "384": hashes.SHA384, "512": hashes.SHA512}
_RSA = {f"{prefix}{bits}" for prefix in ("RS", "PS") for bits in _HASH}
_PRIVATE = {"d", "p", "q", "dp", "dq", "qi", "oth", "k"}


def _component(jwk, name):
    value = jwk.get(name)
    if not isinstance(value, str) or not value:
        raise ValueError(f"missing JWK {name}")
    result = base64url_decode(value)
    if base64url_encode(result) != value:
        raise ValueError(f"invalid JWK {name}")
    return result


def _integer(jwk, name):
    return int.from_bytes(_component(jwk, name), "big")


def public_jwk_key(jwk: Mapping, algorithm: str):
    if not isinstance(jwk, Mapping) or _PRIVATE.intersection(jwk):
        raise ValueError("expected a public JWK")
    if jwk.get("alg", algorithm) != algorithm or jwk.get("use", "sig") not in {
        "sig",
        "jwt-svid",
        "wit-svid",
    }:
        raise ValueError("JWK is not authorized for the signature algorithm")
    if "key_ops" in jwk and (
        not isinstance(jwk["key_ops"], (list, tuple)) or "verify" not in jwk["key_ops"]
    ):
        raise ValueError("JWK is not authorized for verification")
    if algorithm in _EC and jwk.get("kty") == "EC":
        curve = _EC[algorithm]()
        curves = {"ES256": "P-256", "ES384": "P-384", "ES512": "P-521"}
        width = (curve.key_size + 7) // 8
        if jwk.get("crv") != curves[algorithm] or any(
            len(_component(jwk, name)) != width for name in ("x", "y")
        ):
            raise ValueError(
                "JWK curve or coordinate does not match signature algorithm"
            )
        return ec.EllipticCurvePublicNumbers(
            _integer(jwk, "x"), _integer(jwk, "y"), curve
        ).public_key()
    if algorithm in _RSA and jwk.get("kty") == "RSA":
        key = rsa.RSAPublicNumbers(_integer(jwk, "e"), _integer(jwk, "n")).public_key()
        if key.key_size < 2048:
            raise ValueError("RSA signature keys must be at least 2048 bits")
        return key
    if algorithm in {"EdDSA", "Ed25519", "Ed448"} and jwk.get("kty") == "OKP":
        curves = {"Ed25519": ed25519.Ed25519PublicKey, "Ed448": ed448.Ed448PublicKey}
        curve = jwk.get("crv")
        if curve in curves and algorithm in {"EdDSA", curve}:
            return curves[curve].from_public_bytes(_component(jwk, "x"))
    raise ValueError("unsupported JWK or asymmetric signature algorithm")


def verify_public_jws(serialized: str, jwk: Mapping) -> None:
    jws = parse_jws_compact(serialized)
    headers = jws.protected_headers
    if jws.detached or "crit" in headers or "b64" in headers:
        raise ValueError("unsupported JWT protected header")
    algorithm = headers["alg"]
    key = public_jwk_key(jwk, algorithm)
    signature = jws.signature
    message = jws.signing_input()
    try:
        if isinstance(key, ec.EllipticCurvePublicKey):
            width = (key.curve.key_size + 7) // 8
            if len(signature) != 2 * width:
                raise ValueError("invalid ECDSA JWS signature length")
            signature = utils.encode_dss_signature(
                int.from_bytes(signature[:width], "big"),
                int.from_bytes(signature[width:], "big"),
            )
            key.verify(signature, message, ec.ECDSA(_HASH[algorithm[-3:]]()))
        elif isinstance(key, rsa.RSAPublicKey):
            digest = _HASH[algorithm[-3:]]()
            scheme = (
                padding.PSS(mgf=padding.MGF1(digest), salt_length=digest.digest_size)
                if algorithm.startswith("PS")
                else padding.PKCS1v15()
            )
            key.verify(signature, message, scheme, digest)
        else:
            key.verify(signature, message)
    except InvalidSignature as error:
        raise ValueError("JWS signature verification failed") from error
