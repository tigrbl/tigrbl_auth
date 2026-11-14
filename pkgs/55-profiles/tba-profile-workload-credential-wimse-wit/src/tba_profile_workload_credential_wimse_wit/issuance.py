from collections.abc import Mapping

from tba_protocol_workload_wimse_identifier import WorkloadIdentifier
from tba_provider_jose_cryptography.jws import (
    ProtectedEnvelopeIssuerPort,
    sign_compact_jwt,
)
from tba_provider_jose_cryptography.public_jws import public_jwk_key


def issue_wit(
    signer: ProtectedEnvelopeIssuerPort,
    *,
    subject: str,
    confirmation_jwk: Mapping[str, str],
    issuer_key_reference: str,
    issuer_key_id: str,
    issuer_algorithm: str,
    issued_at: int,
    expires_at: int,
) -> str:
    """Issue a workload credential using the configured trust-domain signer."""
    if (
        type(issued_at) is not int
        or type(expires_at) is not int
        or expires_at <= issued_at
    ):
        raise ValueError("WIT expiry must follow issuance")
    if (
        not issuer_key_id
        or issuer_algorithm.lower() == "none"
        or issuer_algorithm.startswith("HS")
        or not issuer_algorithm
    ):
        raise ValueError("WIT requires an identified asymmetric signing key")
    confirmation = dict(confirmation_jwk)
    algorithm = confirmation.get("alg")
    if not isinstance(algorithm, str):
        raise ValueError("WIT confirmation JWK requires a signing algorithm")
    public_jwk_key(confirmation, algorithm)
    claims = {
        "sub": str(WorkloadIdentifier.parse(subject)),
        "cnf": {"jwk": confirmation},
        "iat": issued_at,
        "exp": expires_at,
    }
    return sign_compact_jwt(
        signer,
        claims,
        headers={"typ": "wit+jwt", "alg": issuer_algorithm, "kid": issuer_key_id},
        key_reference=issuer_key_reference,
    )
