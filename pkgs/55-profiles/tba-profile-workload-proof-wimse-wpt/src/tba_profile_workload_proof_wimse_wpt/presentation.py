from collections.abc import Mapping
from secrets import token_urlsafe

from tba_concrete_jwt import decode_jwt_unverified
from tba_provider_jose_cryptography.jws import (
    ProtectedEnvelopeIssuerPort,
    sign_compact_jwt,
)
from tba_provider_jose_cryptography.public_jws import verify_public_jws

from .verification import _hash_token, _target_audience


def present_wit(
    signer: ProtectedEnvelopeIssuerPort,
    wit: str,
    *,
    workload_key_reference: str,
    target_uri: str,
    now: int,
    lifetime_seconds: int = 60,
) -> dict[str, str]:
    """Sign and present a proof for an already provisioned WIT."""
    if (
        type(now) is not int
        or type(lifetime_seconds) is not int
        or not 0 < lifetime_seconds <= 300
    ):
        raise ValueError("WPT lifetime must be between 1 and 300 seconds")
    token = decode_jwt_unverified(wit)
    if token.jws.protected_headers.get("typ") not in ("wit+jwt", "application/wit+jwt"):
        raise ValueError("expected a WIT")
    confirmation = token.claims.get("cnf")
    jwk = confirmation.get("jwk") if isinstance(confirmation, Mapping) else None
    algorithm = jwk.get("alg") if isinstance(jwk, Mapping) else None
    if not isinstance(algorithm, str):
        raise ValueError("WIT confirmation JWK requires a signing algorithm")
    claims = {
        "aud": _target_audience(target_uri),
        "exp": now + lifetime_seconds,
        "jti": token_urlsafe(16),
        "wth": _hash_token(wit),
    }
    proof = sign_compact_jwt(
        signer,
        claims,
        headers={"typ": "wpt+jwt", "alg": algorithm},
        key_reference=workload_key_reference,
    )
    verify_public_jws(proof, jwk)
    return {"Workload-Identity-Token": wit, "Authorization": f"WPT {proof}"}
