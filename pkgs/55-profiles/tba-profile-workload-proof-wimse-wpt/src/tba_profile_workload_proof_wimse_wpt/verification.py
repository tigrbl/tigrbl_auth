import hashlib
from math import ceil, isfinite
from urllib.parse import urlsplit

from tba_concrete_jwt import decode_jwt_unverified
from tba_primitives_identity import base64url_encode
from tba_profile_workload_credential_wimse_wit import verify_wit
from tba_provider_jose_cryptography.public_jws import verify_public_jws


def _hash_token(value: str) -> str:
    return base64url_encode(hashlib.sha256(value.encode("ascii")).digest())


def _target_audience(uri: str) -> str:
    target = urlsplit(uri)
    if (
        target.scheme not in {"http", "https"}
        or not target.hostname
        or target.username is not None
    ):
        raise ValueError("WPT audience requires an absolute HTTP target URI")
    return target._replace(path=target.path or "/", query="", fragment="").geturl()


def verify_wpt(
    proof: str,
    *,
    wit_serialized: str,
    confirmation_key,
    subject: str,
    audience: str,
    now: float,
    replay_store,
    max_lifetime: int = 300,
    presented_headers=(),
    bound_token_headers=(),
):
    token = decode_jwt_unverified(proof)
    headers = token.jws.protected_headers
    if headers.get("typ") not in ("wpt+jwt", "application/wpt+jwt"):
        raise ValueError("invalid WPT media type")
    if headers["alg"] != confirmation_key.get("alg"):
        raise ValueError("WPT algorithm does not match the confirmation key")
    claims = token.claims
    target = _target_audience(audience)
    audiences = claims.get("aud")
    if isinstance(audiences, str):
        audiences = [audiences]
    if (
        not target
        or not isinstance(audiences, list)
        or not all(isinstance(item, str) for item in audiences)
        or target not in audiences
    ):
        raise ValueError("WPT audience mismatch")
    expires = claims.get("exp")
    if (
        type(expires) not in (int, float)
        or not isfinite(expires)
        or not now < expires <= now + max_lifetime
    ):
        raise ValueError("invalid WPT expiry")
    proof_id = claims.get("jti")
    if (
        not isinstance(proof_id, str)
        or not proof_id
        or claims.get("wth") != _hash_token(wit_serialized)
    ):
        raise ValueError("invalid WPT identifier or WIT binding")
    transaction_tokens = [
        value.strip()
        for name, value in presented_headers
        if name.lower() == "txn-token"
    ]
    if transaction_tokens or "tth" in claims:
        if len(transaction_tokens) != 1 or claims.get("tth") != _hash_token(
            transaction_tokens[0]
        ):
            raise ValueError("WPT transaction token binding mismatch")
    required_bindings = {
        name.lower()
        for name in bound_token_headers
        if any(field.lower() == name.lower() for field, _ in presented_headers)
    }
    if required_bindings or "oth" in claims:
        other = claims.get("oth")
        if not isinstance(other, dict) or not required_bindings.issubset(other):
            raise ValueError("WPT required token binding is missing")
        for name, digest in other.items():
            values = [
                value.strip()
                for field, value in presented_headers
                if field.lower() == name
            ]
            if len(values) != 1 or digest != _hash_token(values[0]):
                raise ValueError("WPT additional token binding mismatch")
    verify_public_jws(proof, confirmation_key)
    replay_key = _hash_token(f"{subject}\n{proof_id}")
    if not replay_store.check_and_store(
        f"wimse-wpt:{replay_key}", now=int(now), ttl_s=ceil(expires) - int(now)
    ):
        raise ValueError("WPT replay rejected")
    return token


def authenticate_wpt_request(
    headers,
    *,
    audience: str,
    trust_by_domain,
    now: float,
    replay_store,
    bound_token_headers=(),
):
    """Authenticate HTTP headers using the application's configured target audience."""
    headers = tuple(headers)
    identity = [
        value.strip()
        for name, value in headers
        if name.lower() == "workload-identity-token"
    ]
    authorization = [
        value.strip() for name, value in headers if name.lower() == "authorization"
    ]
    if len(identity) != 1 or len(authorization) != 1:
        raise ValueError("expected one WIT header and one WPT authorization")
    scheme, separator, proof = authorization[0].partition(" ")
    if scheme.lower() != "wpt" or not separator or not proof.strip():
        raise ValueError("expected WPT authorization")
    wit = verify_wit(identity[0], trust_by_domain=trust_by_domain, now=now)
    verify_wpt(
        proof.strip(),
        wit_serialized=identity[0],
        confirmation_key=wit.claims["cnf"]["jwk"],
        subject=wit.claims["sub"],
        audience=audience,
        now=now,
        replay_store=replay_store,
        presented_headers=headers,
        bound_token_headers=bound_token_headers,
    )
    return wit
