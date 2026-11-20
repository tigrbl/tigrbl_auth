from tba_concrete_eat import EatClaimSetPayload, EatEncoding, parse_eat_claims
from tba_concrete_sd_jwt import KeyBindingClaimSetPayload, parse_key_binding_claims
from tba_profile_credential_sd_jwt_vc import (
    SdJwtVcClaimSetPayload,
    parse_sd_jwt_vc_claims,
)
from tba_concrete_svid import JwtSvidClaimSetPayload, parse_jwt_svid_claims


def test_aggregate_payload_models_are_explicitly_claim_sets() -> None:
    assert isinstance(
        parse_eat_claims({"eat_profile": "urn:example:eat"}, EatEncoding.JSON),
        EatClaimSetPayload,
    )
    assert isinstance(
        parse_sd_jwt_vc_claims({"vct": "urn:example:credential"}),
        SdJwtVcClaimSetPayload,
    )
    assert isinstance(
        parse_jwt_svid_claims(
            {"sub": "spiffe://example.org/workload", "aud": "service", "exp": 10}
        ),
        JwtSvidClaimSetPayload,
    )
    assert isinstance(
        parse_key_binding_claims(
            {"aud": "verifier", "nonce": "n", "iat": 1, "sd_hash": "h"}
        ),
        KeyBindingClaimSetPayload,
    )
