from tigrbl_digital_credential_issuer_local import LocalDigitalCredentialIssuer
from tigrbl_digital_credential_status_provider import InMemoryCredentialStatusProvider
from tigrbl_digital_credential_trust_provider import PinnedIssuerTrustProvider
from tigrbl_digital_presentation_verifier import DispatchingPresentationVerifier
from tigrbl_identity_contracts.digital_credentials import (
    CredentialConfiguration,
    CredentialFormat,
    CredentialIssuanceRequest,
    CredentialIssuanceResult,
    CredentialStatusReference,
    CredentialType,
    DigitalCredential,
    PresentationRequest,
    PresentationResult,
    TransactionBinding,
)


def test_local_issuer_dispatches_by_configuration_and_enforces_format():
    format_ = CredentialFormat("dc+sd-jwt", "application/dc+sd-jwt")
    configuration = CredentialConfiguration(
        "employee",
        CredentialType("urn:example:employee", format_),
        (format_,),
    )
    issuer = LocalDigitalCredentialIssuer()
    issuer.register(
        configuration,
        lambda request: CredentialIssuanceResult(
            DigitalCredential(
                request.format, "encoded", issuer="https://issuer.example"
            )
        ),
    )
    result = issuer.issue(
        CredentialIssuanceRequest("employee", format_, subject="alice")
    )
    assert result.credential is not None and result.credential.format == format_


def test_status_provider_defaults_to_unknown_and_publishes_lifecycle_state():
    reference = CredentialStatusReference("status-list", "https://issuer/status", 4)
    provider = InMemoryCredentialStatusProvider()
    assert provider.resolve(reference) == "unknown"
    provider.publish(reference, "revoked")
    assert provider.resolve(reference) == "revoked"


def test_issuer_trust_is_explicit_and_profile_scoped():
    provider = PinnedIssuerTrustProvider()
    provider.trust("https://issuer.example", "sd-jwt-vc")
    assert provider.resolve("https://issuer.example", "sd-jwt-vc").trusted
    assert not provider.resolve("https://issuer.example", "mdoc-issuer").trusted


def test_presentation_verifier_dispatches_only_to_accepted_registered_formats():
    verifier = DispatchingPresentationVerifier()
    verifier.register(
        "dc+sd-jwt",
        lambda value, request: PresentationResult(
            value == "valid", disclosed_claims={"name": "Alice"}
        ),
    )
    request = PresentationRequest(
        ("dc+sd-jwt",),
        TransactionBinding("nonce", "https://verifier.example"),
    )
    assert verifier.verify("valid", request).valid
    unsupported = PresentationRequest(
        ("mso_mdoc",),
        TransactionBinding("nonce", "https://verifier.example"),
    )
    assert not verifier.verify("valid", unsupported).valid
