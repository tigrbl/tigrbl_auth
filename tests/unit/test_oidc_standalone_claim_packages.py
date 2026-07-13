from pathlib import Path

from tigrbl_auth_protocol_oidc import (
    OIDC_ID_TOKEN_PROFILE_CLAIMS,
    OIDC_USERINFO_CLAIMS,
    compose_oidc_id_token_claim_set,
    compose_oidc_userinfo_claim_set,
)
from tigrbl_claim_email_concrete import EmailClaim
from tigrbl_claim_email_verified_concrete import EmailVerifiedClaim
from tigrbl_claim_name_concrete import NameClaim
from tigrbl_identity_claims_bases import ClaimBase

ROOT = Path(__file__).resolve().parents[2]


def test_oidc_core_claims_are_standalone_layer_10_packages():
    expected = {claim.claim_name for claim in OIDC_USERINFO_CLAIMS} | {
        claim.claim_name for claim in OIDC_ID_TOKEN_PROFILE_CLAIMS
    }
    assert expected >= {
        "name", "given_name", "family_name", "middle_name", "nickname",
        "preferred_username", "profile", "picture", "website", "email",
        "email_verified", "gender", "birthdate", "zoneinfo", "locale",
        "phone_number", "phone_number_verified", "address", "updated_at",
        "auth_time", "nonce", "acr", "amr", "azp", "at_hash", "c_hash",
        "s_hash", "sid",
    }
    for claim_class in (*OIDC_USERINFO_CLAIMS, *OIDC_ID_TOKEN_PROFILE_CLAIMS):
        assert issubclass(claim_class, ClaimBase)
        package = claim_class.__module__.replace("_", "-")
        assert (ROOT / "pkgs" / "10-concrete" / package / "pyproject.toml").is_file()


def test_oidc_core_value_shapes_and_versioned_sets():
    assert NameClaim("Alice").name == "name"
    assert EmailClaim("alice@example.test").name == "email"
    assert EmailVerifiedClaim(True).value is True
    assert compose_oidc_userinfo_claim_set(NameClaim("Alice")).version == "1.0-errata2"
    assert compose_oidc_id_token_claim_set().protocol == "oidc-id-token"
