from tigrbl_eat_concrete import EatClaimSetPayload, EatEncoding, parse_eat_claims
from tigrbl_sd_jwt_concrete import KeyBindingClaimSetPayload, parse_key_binding_claims
from tigrbl_credential_profile_sd_jwt_vc import (
    SdJwtVcClaimSetPayload,
    parse_sd_jwt_vc_claims,
)
from tigrbl_svid_concrete import JwtSvidClaimSetPayload, parse_jwt_svid_claims


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
