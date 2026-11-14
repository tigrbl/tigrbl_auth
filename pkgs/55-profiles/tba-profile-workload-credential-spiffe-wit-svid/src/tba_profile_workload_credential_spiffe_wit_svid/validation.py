from collections.abc import Mapping
from math import isfinite
from time import time

from tba_contracts_proof_of_possession import PossessionProofVerificationResult
from tba_protocol_workload_spiffe_svid import validate_spiffe_id


ECDSA_CURVES = {"ES256": "P-256", "ES384": "P-384", "ES512": "P-521"}
RSA_ALGORITHMS = frozenset({"RS256", "RS384", "RS512", "PS256", "PS384", "PS512"})
ALLOWED_ALGORITHMS = frozenset(ECDSA_CURVES) | RSA_ALGORITHMS
PRIVATE_JWK_FIELDS = frozenset({"d", "p", "q", "dp", "dq", "qi", "oth", "k"})


def _is_numeric_date(value: object) -> bool:
    return type(value) is int or (type(value) is float and isfinite(value))


def _validate_confirmation_key(confirmation: object) -> None:
    jwk = confirmation.get("jwk") if isinstance(confirmation, Mapping) else None
    if not isinstance(jwk, Mapping) or PRIVATE_JWK_FIELDS.intersection(jwk):
        raise ValueError("WIT-SVID requires a public confirmation JWK")
    algorithm = jwk.get("alg")
    if not isinstance(algorithm, str) or algorithm not in ALLOWED_ALGORITHMS:
        raise ValueError("WIT-SVID confirmation key algorithm is not permitted")
    if algorithm in ECDSA_CURVES:
        if jwk.get("kty") != "EC" or jwk.get("crv") != ECDSA_CURVES[algorithm]:
            raise ValueError("WIT-SVID confirmation key does not match its algorithm")
        fields = ("x", "y")
    else:
        if jwk.get("kty") != "RSA":
            raise ValueError("WIT-SVID confirmation key does not match its algorithm")
        fields = ("n", "e")
    if any(not isinstance(jwk.get(field), str) or not jwk[field] for field in fields):
        raise ValueError("WIT-SVID confirmation key is incomplete")


def validate_wit_svid_claims(
    headers: Mapping[str, object],
    claims: Mapping[str, object],
    *,
    now: float | None = None,
) -> None:
    """Check the profile after the caller verifies the JWS and its bound proof.

    The caller selects issuer keys from the SPIFFE trust bundle and verifies
    proof against the confirmation key of this credential and its presentation.
    """
    if headers.get("typ") != "wit+jwt":
        raise ValueError("WIT-SVID requires typ=wit+jwt")
    if not isinstance(headers.get("kid"), str) or not headers["kid"]:
        raise ValueError("WIT-SVID requires kid")
    algorithm = headers.get("alg")
    if not isinstance(algorithm, str) or algorithm not in ALLOWED_ALGORITHMS:
        raise ValueError("WIT-SVID algorithm is not permitted")
    missing = {"sub", "cnf", "exp"}.difference(claims)
    if missing:
        raise ValueError(f"missing WIT-SVID claims: {sorted(missing)}")
    subject = claims["sub"]
    if not isinstance(subject, str):
        raise ValueError("WIT-SVID subject must be a SPIFFE ID")
    validate_spiffe_id(subject)
    if "aud" in claims:
        raise ValueError("WIT-SVID must not contain aud")
    for name in ("iss", "jti"):
        if name in claims and not isinstance(claims[name], str):
            raise ValueError(f"WIT-SVID {name} must be a string")
    for name in ("exp", "nbf", "iat"):
        if name in claims and not _is_numeric_date(claims[name]):
            raise ValueError(f"WIT-SVID {name} must be a NumericDate")
    current_time = time() if now is None else now
    if not _is_numeric_date(current_time):
        raise ValueError("WIT-SVID validation time must be a NumericDate")
    if current_time >= claims["exp"]:
        raise ValueError("WIT-SVID has expired")
    if "nbf" in claims and current_time < claims["nbf"]:
        raise ValueError("WIT-SVID is not yet valid")
    _validate_confirmation_key(claims["cnf"])


def validate_wit_svid(
    headers, claims, *, proof_result: PossessionProofVerificationResult, now=None
):
    validate_wit_svid_claims(headers, claims, now=now)
    subject = claims["sub"]
    if not proof_result.valid or proof_result.replay_accepted is not True:
        raise ValueError(
            "WIT-SVID requires verified, replay-accepted proof of possession"
        )
    if proof_result.subject is not None and proof_result.subject != subject:
        raise ValueError("WIT-SVID proof subject does not match")
