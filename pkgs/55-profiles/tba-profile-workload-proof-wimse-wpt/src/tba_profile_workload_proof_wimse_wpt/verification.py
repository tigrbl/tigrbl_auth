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
    # Keep the public subject argument for existing callers. The replay key uses
    # the signed WIT digest, which is also available to the carrier-neutral port.
    token_digests = {}
    for name, value in presented_headers:
        name = name.lower()
        token_digests[name] = None if name in token_digests else value.strip()
    required = {name.lower() for name in bound_token_headers}
    return _verify_wpt(
        proof,
        wit_digest=_hash_token(wit_serialized),
        confirmation_key=confirmation_key,
        audience=audience,
        now=now,
        replay_store=replay_store,
        max_lifetime=max_lifetime,
        token_digests=token_digests,
        required=required,
        digest_values=True,
    )


def _verify_wpt(
    proof,
    *,
    wit_digest,
    confirmation_key,
    audience,
    now,
    replay_store,
    token_digests,
    max_lifetime=300,
    required=(),
    digest_values=False,
    expected_proof_id=None,
):
    token = decode_jwt_unverified(proof)
    headers = token.jws.protected_headers
    if headers.get("typ") not in ("wpt+jwt", "application/wpt+jwt"):
        raise ValueError("invalid WPT media type")
    if not headers.get("alg") or headers["alg"] != confirmation_key.get("alg"):
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
        or (expected_proof_id is not None and proof_id != expected_proof_id)
        or claims.get("wth") != wit_digest
    ):
        raise ValueError("invalid WPT identifier or WIT binding")

    def digest(name):
        value = token_digests.get(name)
        return _hash_token(value) if digest_values and value is not None else value

    if any(not digest(name) for name in required):
        raise ValueError("WPT required token binding is missing")
    required = set(required) - {"txn-token"}

    if "txn-token" in token_digests or "tth" in claims:
        transaction_digest = digest("txn-token")
        if not transaction_digest or claims.get("tth") != transaction_digest:
            raise ValueError("WPT transaction token binding mismatch")
    if required or "oth" in claims:
        other = claims.get("oth")
        if not isinstance(other, dict) or not set(required).issubset(other):
            raise ValueError("WPT required token binding is missing")
        for name, expected_digest in other.items():
            actual_digest = digest(name)
            if not actual_digest or expected_digest != actual_digest:
                raise ValueError("WPT additional token binding mismatch")
    verify_public_jws(proof, confirmation_key)
    replay_key = base64url_encode(
        hashlib.sha256(f"{wit_digest}\n{proof_id}".encode()).digest()
    )
    accepted = replay_store.check_and_store(
        f"wimse-wpt:{replay_key}", now=int(now), ttl_s=ceil(expires) - int(now)
    )
    if accepted is not True:
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
