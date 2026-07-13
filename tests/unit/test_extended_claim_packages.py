import importlib

import pytest

from tigrbl_attestation_protocol_eat import EAT_CLAIM_CLASSES
from tigrbl_auth_protocol_oauth import (
    OAUTH_DPOP_PROOF_CLAIMS,
    OAUTH_TOKEN_EXCHANGE_CLAIMS,
    compose_dpop_proof_claim_set,
    compose_token_exchange_claim_set,
)
from tigrbl_identity_claims_bases import ClaimBase


PACKAGES = {
    "tigrbl_claim_http_method_concrete": "HttpMethodClaim",
    "tigrbl_claim_http_uri_concrete": "HttpUriClaim",
    "tigrbl_claim_access_token_hash_concrete": "AccessTokenHashClaim",
    "tigrbl_claim_sd_hash_concrete": "SdHashClaim",
    "tigrbl_claim_eat_nonce_concrete": "EatNonceClaim",
    "tigrbl_claim_ueid_concrete": "UeidClaim",
    "tigrbl_claim_eat_submodules_concrete": "EatSubmodulesClaim",
    "tigrbl_claim_actor_concrete": "ActorClaim",
    "tigrbl_claim_may_act_concrete": "MayActClaim",
}


def test_each_extended_claim_is_a_standalone_claimbase_package():
    for package, class_name in PACKAGES.items():
        claim_class = getattr(importlib.import_module(package), class_name)
        assert issubclass(claim_class, ClaimBase)
        assert claim_class.__module__ == package


def test_protocols_compose_extended_claim_families():
    assert {claim.claim_name for claim in OAUTH_DPOP_PROOF_CLAIMS} == {
        "jti", "htm", "htu", "iat", "nonce", "ath"
    }
    assert {claim.claim_name for claim in OAUTH_TOKEN_EXCHANGE_CLAIMS} == {"act", "may_act"}
    assert {claim.claim_name for claim in EAT_CLAIM_CLASSES} >= {
        "eat_profile", "eat_nonce", "iat", "ueid", "submods"
    }


def test_extended_protocol_claim_sets_are_explicitly_versioned():
    from tigrbl_claim_actor_concrete import ActorClaim
    from tigrbl_claim_http_method_concrete import HttpMethodClaim

    assert compose_dpop_proof_claim_set(HttpMethodClaim("POST")).version == "RFC9449"
    assert compose_token_exchange_claim_set(ActorClaim({"sub": "alice"})).version == "RFC8693"


@pytest.mark.parametrize(
    ("module", "class_name", "bad_value"),
    [
        ("tigrbl_claim_http_method_concrete", "HttpMethodClaim", "post"),
        ("tigrbl_claim_http_uri_concrete", "HttpUriClaim", "/token"),
        ("tigrbl_claim_access_token_hash_concrete", "AccessTokenHashClaim", ""),
        ("tigrbl_claim_eat_nonce_concrete", "EatNonceClaim", []),
        ("tigrbl_claim_ueid_concrete", "UeidClaim", 3),
        ("tigrbl_claim_eat_submodules_concrete", "EatSubmodulesClaim", []),
        ("tigrbl_claim_actor_concrete", "ActorClaim", {}),
        ("tigrbl_claim_may_act_concrete", "MayActClaim", {}),
    ],
)
def test_extended_claims_reject_invalid_shapes(module, class_name, bad_value):
    with pytest.raises(ValueError):
        getattr(importlib.import_module(module), class_name)(bad_value)
