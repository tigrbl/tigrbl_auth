import pytest

from tigrbl_authentication_assurance_bases import (
    AuthenticationContextEvaluatorBase,
    IdentityAssuranceClaimsProviderBase,
    VerifiedClaimsValidatorBase,
)
from tigrbl_identity_contracts.assurance import VerifiedClaimsRequest
from tigrbl_identity_contracts.oidc import (
    IDENTITY_ASSURANCE_CLAIM_NAMES,
    AuthenticatorEvidence,
    EapAcrEvaluationRequest,
    EapAcrValue,
    EapAmrValue,
    IdentityAssuranceClaims,
    IdentityAssuranceRequest,
    PlaceOfBirth,
)


def test_eap_acr_contract_defines_all_standard_values_and_normalized_evidence():
    evidence = AuthenticatorEvidence(
        phishing_resistant=True,
        hardware_protected=True,
        user_verified=True,
        proof_of_possession=True,
        methods=("hwk",),
    )
    request = EapAcrEvaluationRequest(
        (EapAcrValue.PHISHING_RESISTANT_HARDWARE,), (evidence,)
    )
    assert {value.value for value in EapAcrValue} == {"phr", "phrh"}
    assert {value.value for value in EapAmrValue} == {"pop"}
    assert request.evidence[0].hardware_protected


def test_identity_assurance_claim_registry_contains_required_claims():
    required = {
        "verified_claims",
        "place_of_birth",
        "nationalities",
        "birth_family_name",
        "birth_given_name",
        "birth_middle_name",
        "salutation",
        "title",
        "msisdn",
        "also_known_as",
        "address.country_code",
    }
    assert set(IDENTITY_ASSURANCE_CLAIM_NAMES) == required
    claims = IdentityAssuranceClaims({"place_of_birth": PlaceOfBirth(country="US")})
    assert claims.values["place_of_birth"].country == "US"


def test_identity_assurance_claim_contract_rejects_unregistered_names():
    with pytest.raises(ValueError, match="unregistered"):
        IdentityAssuranceClaims({"favorite_color": "blue"})


def test_identity_assurance_request_is_independent_of_token_transport():
    request = IdentityAssuranceRequest(
        VerifiedClaimsRequest({"given_name": None}), purpose="kyc"
    )
    assert request.purpose == "kyc"
    assert not hasattr(request, "id_token")


def test_neutral_assurance_bases_implement_typed_contracts():
    assert all(
        isinstance(base, type)
        for base in (
            AuthenticationContextEvaluatorBase,
            IdentityAssuranceClaimsProviderBase,
            VerifiedClaimsValidatorBase,
        )
    )
