from datetime import datetime, timezone

from tigrbl_identity_contracts.digital_credentials import (
    CredentialFormat,
    CredentialIssuanceRequest,
    CredentialType,
    DigitalCredential,
    PresentationRequest,
    TransactionBinding,
)
from tigrbl_identity_contracts.security_events import (
    SecurityEvent,
    SecurityEventSubject,
)
from tigrbl_identity_contracts.tokens import TokenProfile, TokenVerificationRequest
from tigrbl_security_trust_contracts import (
    CertificateArtifact,
    CertificatePathValidationRequest,
    CertificateProfile,
    TrustAnchor,
)


def test_digital_credential_contracts_remain_format_neutral():
    format_ = CredentialFormat("dc+sd-jwt", "application/dc+sd-jwt")
    credential_type = CredentialType("urn:example:employee", format_)
    credential = DigitalCredential(format_, "encoded", issuer="https://issuer.example")
    request = CredentialIssuanceRequest("employee", format_, subject="alice")
    presentation = PresentationRequest(
        (format_.identifier,),
        TransactionBinding("nonce", "https://verifier.example"),
    )

    assert credential_type.format is format_
    assert credential.format is request.format
    assert presentation.binding.nonce == "nonce"


def test_profiled_token_contract_requires_expected_profile():
    request = TokenVerificationRequest("token", TokenProfile.SECURITY_EVENT_TOKEN)
    assert request.expected_profile is TokenProfile.SECURITY_EVENT_TOKEN


def test_security_event_contract_models_subject_separately():
    event = SecurityEvent(
        "https://schemas.example/account-disabled",
        "https://issuer.example",
        ("receiver",),
        "event-1",
        datetime.now(timezone.utc),
        SecurityEventSubject("iss_sub", {"iss": "issuer", "sub": "alice"}),
    )
    assert event.subject is not None and event.subject.format == "iss_sub"


def test_certificate_validation_contract_selects_a_profile():
    artifact = CertificateArtifact(b"certificate", CertificateProfile.X509_SVID)
    request = CertificatePathValidationRequest(artifact)
    anchor = TrustAnchor("root", b"root", (CertificateProfile.X509_SVID,))

    assert request.leaf.profile == CertificateProfile.X509_SVID
    assert CertificateProfile.X509_SVID in anchor.profiles
