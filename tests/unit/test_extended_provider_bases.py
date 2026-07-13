from tigrbl_attestation_bases import (
    AttestationAppraiserBase,
    EvidenceVerifierBase,
    ReferenceMaterialProviderBase,
)
from tigrbl_authentication_assurance_bases import (
    AuthenticationContextEvaluatorBase,
    IdentityAssuranceClaimsProviderBase,
    VerifiedClaimsValidatorBase,
)
from tigrbl_digital_credential_bases import (
    CredentialIssuerBase,
    CredentialStatusResolverBase,
    CredentialVerifierBase,
    PresentationVerifierBase,
    WalletAttestationVerifierBase,
)
from tigrbl_identity_authenticator_bases import (
    AuthenticatorEvidenceEvaluatorBase,
    HardwareKeyProtectionEvaluatorBase,
    PhishingResistanceEvaluatorBase,
)
from tigrbl_jose_bases import (
    EatJwtCoderBase,
    SdJwtCoderBase,
    SdJwtDisclosureVerifierBase,
    SdJwtKeyBindingVerifierBase,
    SetCoderBase,
    WalletAttestationJwtVerifierBase,
)
from tigrbl_authentication_assurance_bases import (
    AuthenticationContextEvaluatorBase as EapAcrEvaluatorBase,
)
from tigrbl_token_bases import ProfiledTokenVerifierBase
from tigrbl_security_event_bases import (
    SecurityEventDeliveryBase,
    SecurityEventReceiverBase,
    SecurityEventReplayBase,
    SecurityEventTransmitterBase,
)
from tigrbl_token_bases import ProfiledTokenIssuerBase


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
    assert ProfiledTokenVerifierBase.__module__ == "tigrbl_token_bases"


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
