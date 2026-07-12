from tigrbl_local_claims_provider_concrete import LocalClaimsProvider


def test_claims_provider_has_standalone_owner() -> None:
    assert LocalClaimsProvider.__module__ == "tigrbl_local_claims_provider_concrete"
