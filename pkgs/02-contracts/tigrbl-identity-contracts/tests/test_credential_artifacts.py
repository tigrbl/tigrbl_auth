from tigrbl_identity_contracts.credential_artifacts import (
    CredentialArtifact,
    PresentationArtifact,
    VerificationRequest,
)


def test_format_independent_artifacts_preserve_binding_inputs() -> None:
    credential = CredentialArtifact("dc+sd-jwt", "issuer~disclosure~", "application/dc+sd-jwt")
    presentation = PresentationArtifact((credential,), audience="https://verifier.example", nonce="n-1")
    request = VerificationRequest(presentation, expected_audience="https://verifier.example", expected_nonce="n-1")
    assert request.artifact.credentials[0].format == "dc+sd-jwt"
