from tba_bases_attestation import (
    AttestationAppraiserBase,
    EvidenceVerifierBase,
    ReferenceMaterialProviderBase,
)
from tba_bases_authentication_assurance import (
    AuthenticationContextEvaluatorBase,
    IdentityAssuranceClaimsProviderBase,
    VerifiedClaimsValidatorBase,
)
from tba_bases_digital_credential import (
    CredentialIssuerBase,
    CredentialStatusResolverBase,
    CredentialVerifierBase,
    PresentationVerifierBase,
    WalletAttestationVerifierBase,
)
from tba_bases_identity_authenticator import (
    AuthenticatorEvidenceEvaluatorBase,
    HardwareKeyProtectionEvaluatorBase,
    PhishingResistanceEvaluatorBase,
)
from tba_bases_jose import (
    EatJwtCoderBase,
    SdJwtCoderBase,
    SdJwtDisclosureVerifierBase,
    SdJwtKeyBindingVerifierBase,
    SetCoderBase,
    WalletAttestationJwtVerifierBase,
)
from tba_bases_authentication_assurance import (
    AuthenticationContextEvaluatorBase as EapAcrEvaluatorBase,
)
from tba_bases_token import ProfiledTokenVerifierBase
from tba_bases_security_event import (
    SecurityEventDeliveryBase,
    SecurityEventReceiverBase,
    SecurityEventReplayBase,
    SecurityEventTransmitterBase,
)
from tba_bases_token import ProfiledTokenIssuerBase


def test_digital_credential_and_attestation_base_surfaces_are_importable():
    bases = (
        CredentialIssuerBase,
        CredentialVerifierBase,
        PresentationVerifierBase,
        CredentialStatusResolverBase,
        WalletAttestationVerifierBase,
        EvidenceVerifierBase,
        AttestationAppraiserBase,
        ReferenceMaterialProviderBase,
    )
    assert all(isinstance(base, type) for base in bases)


def test_token_and_security_event_bases_are_profile_neutral():
    bases = (
        ProfiledTokenIssuerBase,
        ProfiledTokenVerifierBase,
        SecurityEventTransmitterBase,
        SecurityEventReceiverBase,
        SecurityEventDeliveryBase,
        SecurityEventReplayBase,
    )
    assert all(isinstance(base, type) for base in bases)


def test_oidc_and_oauth_names_are_compatibility_exports_of_neutral_bases():
    assert EapAcrEvaluatorBase is AuthenticationContextEvaluatorBase
    assert ProfiledTokenVerifierBase.__module__ == "tba_bases_token"


def test_jose_and_authenticator_extension_points_are_explicit():
    bases = (
        SdJwtCoderBase,
        SdJwtDisclosureVerifierBase,
        SdJwtKeyBindingVerifierBase,
        SetCoderBase,
        EatJwtCoderBase,
        WalletAttestationJwtVerifierBase,
        AuthenticatorEvidenceEvaluatorBase,
        PhishingResistanceEvaluatorBase,
        HardwareKeyProtectionEvaluatorBase,
        IdentityAssuranceClaimsProviderBase,
        VerifiedClaimsValidatorBase,
    )
    assert all(isinstance(base, type) for base in bases)
