from tigrbl_oidc_claims_concrete import (
    EapAcrValue,
    parse_verified_claims,
    serialize_verified_claims,
    satisfies_eap_acr,
)


def test_phrh_satisfies_phr_but_not_the_reverse() -> None:
    assert satisfies_eap_acr(requested="phr", achieved=["phrh"])
    assert not satisfies_eap_acr(requested="phrh", achieved=["phr"])
    assert EapAcrValue.PHISHING_RESISTANT == "phr"


def test_verified_claims_round_trip() -> None:
    source = {
        "verification": {
            "trust_framework": "example",
            "assurance_level": "high",
            "evidence": [{"type": "document", "method": "pipp"}],
        },
        "claims": {"given_name": "Max", "family_name": "Meier"},
    }
    assert serialize_verified_claims(parse_verified_claims(source)) == source


def test_verified_claims_rejects_missing_trust_framework() -> None:
    try:
        parse_verified_claims({"verification": {}, "claims": {}})
    except ValueError as exc:
        assert "trust_framework" in str(exc)
    else:
        raise AssertionError("invalid verified_claims accepted")
