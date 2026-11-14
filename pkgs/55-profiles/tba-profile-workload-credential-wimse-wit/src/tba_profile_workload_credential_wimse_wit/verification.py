from collections.abc import Mapping
from math import isfinite

from dataclasses import replace

from tba_concrete_jwt import decode_jwt_unverified
from tba_concrete_wit import WorkloadIdentityToken
from tba_protocol_workload_wimse_identifier import WorkloadIdentifier
from tba_provider_jose_cryptography.public_jws import public_jwk_key, verify_public_jws


def verify_wit(
    serialized: str, *, trust_by_domain, now: float
) -> WorkloadIdentityToken:
    token = decode_jwt_unverified(serialized)
    headers = token.jws.protected_headers
    if headers.get("typ") not in ("wit+jwt", "application/wit+jwt"):
        raise ValueError("invalid WIT media type")
    claims = token.claims
    identifier = WorkloadIdentifier.parse(claims.get("sub"))
    expiration = claims.get("exp")
    not_before = claims.get("nbf", now)
    if any(
        type(value) not in (int, float) or not isfinite(value)
        for value in (expiration, not_before)
    ):
        raise ValueError("invalid WIT lifetime")
    if not not_before <= now < expiration:
        raise ValueError("WIT is outside its validity period")
    if "iss" in claims and not isinstance(claims["iss"], str):
        raise ValueError("invalid WIT issuer")
    confirmation = claims.get("cnf")
    jwk = confirmation.get("jwk") if isinstance(confirmation, Mapping) else None
    if not isinstance(jwk, Mapping) or not isinstance(jwk.get("alg"), str):
        raise ValueError("WIT requires a public confirmation JWK with an algorithm")
    public_jwk_key(jwk, jwk["alg"])
    keys = tuple(trust_by_domain.get(identifier.trust_domain, ()))
    kid = headers.get("kid")
    if "kid" in headers:
        if not isinstance(kid, str) or not kid:
            raise ValueError("invalid WIT signing key ID")
        keys = tuple(key for key in keys if key.get("kid") == kid)
    if len(keys) != 1:
        raise ValueError(
            "WIT signing key must resolve uniquely within its trust domain"
        )
    verify_public_jws(serialized, keys[0])
    return WorkloadIdentityToken(replace(token, integrity_verified=True))
