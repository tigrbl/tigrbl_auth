import base64
import json
from hashlib import sha256
from hmac import compare_digest
from typing import Mapping

_REQUIRED_MEMBERS = {
    "RSA": ("e", "kty", "n"),
    "EC": ("crv", "kty", "x", "y"),
    "OKP": ("crv", "kty", "x"),
    "oct": ("k", "kty"),
}


def jwk_thumbprint(jwk: Mapping[str, object]) -> str:
    members = _REQUIRED_MEMBERS.get(jwk.get("kty"))
    if members is None:
        raise ValueError(f"unsupported kty: {jwk.get('kty')}")
    try:
        canonical = json.dumps(
            {name: jwk[name] for name in members},
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode()
    except KeyError as exc:
        raise ValueError(f"missing JWK thumbprint member: {exc.args[0]}") from exc
    return (
        base64.urlsafe_b64encode(sha256(canonical).digest())
        .rstrip(b"=")
        .decode("ascii")
    )


def verify_jwk_thumbprint(jwk: Mapping[str, object], thumbprint: str) -> bool:
    try:
        expected = jwk_thumbprint(jwk)
    except (TypeError, ValueError):
        return False
    return compare_digest(expected, thumbprint)


__all__ = ["jwk_thumbprint", "verify_jwk_thumbprint"]
