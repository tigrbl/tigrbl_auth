import importlib

import pytest

from tba_protocol_attestation_eat import EAT_CLAIM_CLASSES
from tba_protocol_oauth import (
    OAUTH_DPOP_PROOF_CLAIMS,
    OAUTH_TOKEN_EXCHANGE_CLAIMS,
    compose_dpop_proof_claim_set,
    compose_token_exchange_claim_set,
)
from tba_bases_identity_claims import ClaimBase


PACKAGES = {
    "tba_concrete_claim_http_method": "HttpMethodClaim",
    "tba_concrete_claim_http_uri": "HttpUriClaim",
    "tba_concrete_claim_access_token_digest": "AccessTokenDigestClaim",
    "tba_concrete_claim_sd_hash": "SdHashClaim",
    "tba_concrete_claim_eat_nonce": "EatNonceClaim",
    "tba_concrete_claim_ueid": "UeidClaim",
    "tba_concrete_claim_eat_submodules": "EatSubmodulesClaim",
    "tba_concrete_claim_actor": "ActorClaim",
    "tba_concrete_claim_may_act": "MayActClaim",
}


def test_each_extended_claim_is_a_standalone_claimbase_package():
    for package, class_name in PACKAGES.items():
        claim_class = getattr(importlib.import_module(package), class_name)
        assert issubclass(claim_class, ClaimBase)
        assert claim_class.__module__ == package


def test_protocols_compose_extended_claim_families():
    assert {claim.claim_name for claim in OAUTH_DPOP_PROOF_CLAIMS} == {
        "jti",
        "htm",
        "htu",
        "iat",
        "nonce",
        "ath",
    }
    assert {claim.claim_name for claim in OAUTH_TOKEN_EXCHANGE_CLAIMS} == {
        "act",
        "may_act",
    }
    assert {claim.claim_name for claim in EAT_CLAIM_CLASSES} >= {
        "eat_profile",
        "eat_nonce",
        "iat",
        "ueid",
        "submods",
    }


def test_extended_protocol_claim_sets_are_explicitly_versioned():
    from tba_concrete_claim_actor import ActorClaim
    from tba_concrete_claim_http_method import HttpMethodClaim

    assert compose_dpop_proof_claim_set(HttpMethodClaim("POST")).version == "RFC9449"
    assert (
        compose_token_exchange_claim_set(ActorClaim({"sub": "alice"})).version
        == "RFC8693"
    )
    with pytest.raises(ValueError, match="not valid for dpop-proof"):
        compose_dpop_proof_claim_set(ActorClaim({"sub": "alice"}))


@pytest.mark.parametrize(
    ("module", "class_name", "bad_value"),
    [
        ("tba_concrete_claim_http_method", "HttpMethodClaim", "post"),
        ("tba_concrete_claim_http_uri", "HttpUriClaim", "/token"),
        ("tba_concrete_claim_access_token_digest", "AccessTokenDigestClaim", ""),
        ("tba_concrete_claim_eat_nonce", "EatNonceClaim", []),
        ("tba_concrete_claim_ueid", "UeidClaim", 3),
        ("tba_concrete_claim_eat_submodules", "EatSubmodulesClaim", []),
        ("tba_concrete_claim_actor", "ActorClaim", {}),
        ("tba_concrete_claim_may_act", "MayActClaim", {}),
    ],
)
def test_extended_claims_reject_invalid_shapes(module, class_name, bad_value):
    with pytest.raises(ValueError):
        getattr(importlib.import_module(module), class_name)(bad_value)
