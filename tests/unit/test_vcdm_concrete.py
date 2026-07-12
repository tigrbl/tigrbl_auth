import pytest
from tigrbl_vcdm_concrete import (
    VCDM_2_RECOMMENDATION,
    parse_verifiable_credential,
    parse_verifiable_presentation,
    validate_verifiable_credential,
    validate_verifiable_presentation,
)


def _credential():
    return {
        "@context": ["https://www.w3.org/ns/credentials/v2"],
        "type": ["VerifiableCredential", "EmployeeCredential"],
        "issuer": "https://issuer.example",
        "credentialSubject": {"id": "did:example:alice", "role": "Engineer"},
        "credentialStatus": {
            "id": "https://issuer.example/status/1#4",
            "type": "BitstringStatusListEntry",
        },
        "credentialSchema": {
            "id": "https://issuer.example/schema/employee",
            "type": "JsonSchema",
        },
        "proof": {"type": "DataIntegrityProof"},
    }


def test_vcdm_2_credential_models_claims_issuer_status_schema_and_proof_container():
    credential = parse_verifiable_credential(_credential())
    validate_verifiable_credential(credential)
    assert credential.credential_subjects[0]["role"] == "Engineer"
    assert credential.status[0].status_type == "BitstringStatusListEntry"
    assert VCDM_2_RECOMMENDATION == "W3C Recommendation 15 May 2025"


def test_vcdm_context_and_proof_shape_are_validated_without_claiming_crypto_validity():
    value = _credential()
    value["@context"] = ["https://example.org/context"]
    with pytest.raises(ValueError, match="base context"):
        validate_verifiable_credential(value)
    value = _credential()
    value["proof"] = {"created": "2026-01-01"}
    with pytest.raises(ValueError, match="proof"):
        validate_verifiable_credential(value)


def test_verifiable_presentation_is_a_container_for_credentials_not_a_credential_itself():
    presentation = parse_verifiable_presentation(
        {
            "@context": ["https://www.w3.org/ns/credentials/v2"],
            "type": ["VerifiablePresentation"],
            "holder": "did:example:alice",
            "verifiableCredential": [_credential()],
            "proof": {"type": "DataIntegrityProof"},
        }
    )
    validate_verifiable_presentation(presentation)
    assert len(presentation.credentials) == 1
    assert not hasattr(presentation, "credential_subjects")


def test_vcdm_structural_validation_does_not_make_issuer_trust_decisions():
    credential = parse_verifiable_credential(_credential())
    validate_verifiable_credential(credential)
    assert not hasattr(credential, "trusted")
