from tba_concrete_jwt import decode_jwt_unverified
from tba_profile_workload_proof_wimse_wpt import verify_wpt
from tba_protocol_workload_spiffe_svid import validate_spiffe_id
from tba_provider_jose_cryptography.public_jws import verify_public_jws

from .validation import validate_wit_svid_claims


def verify_wit_svid(
    serialized,
    proof,
    *,
    audience,
    keys_by_domain,
    now,
    replay_store,
    presented_headers=(),
):
    token = decode_jwt_unverified(serialized)
    headers = token.jws.protected_headers
    validate_wit_svid_claims(headers, token.claims, now=now)
    subject = token.claims["sub"]
    domain, path = validate_spiffe_id(subject)
    if not path:
        raise ValueError("WIT-SVID requires a workload identity")
    keys = [
        key
        for key in keys_by_domain.get(domain, ())
        if key.get("kid") == headers["kid"] and key.get("use") == "wit-svid"
    ]
    if len(keys) != 1:
        raise ValueError("WIT-SVID signing key must resolve within its trust bundle")
    verify_public_jws(serialized, keys[0])
    verify_wpt(
        proof,
        wit_serialized=serialized,
        confirmation_key=token.claims["cnf"]["jwk"],
        subject=subject,
        audience=audience,
        now=now,
        replay_store=replay_store,
        presented_headers=presented_headers,
    )
    return subject
