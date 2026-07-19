from tigrbl_cose_bases import (
    CoseEnvelopeIssuerBase,
    CoseEnvelopeVerifierBase,
    CwtTokenIssuerBase,
    CwtTokenVerifierBase,
)
from tigrbl_identity_document_bases import (
    IdentityDocumentPublisherBase,
    IdentityDocumentResolverBase,
    IdentityDocumentVerifierBase,
)
from tigrbl_identity_document_contracts import (
    IdentityDocumentPublisherPort,
    IdentityDocumentResolverPort,
    IdentityDocumentVerifierPort,
)
from tigrbl_jose_bases import (
    JoseEnvelopeIssuerBase,
    JoseEnvelopeVerifierBase,
    JwtTokenIssuerBase,
    JwtTokenVerifierBase,
)
from tigrbl_proof_of_possession_bases import (
    ConfirmationKeyResolverBase,
    PossessionProofIssuerBase,
    PossessionProofVerifierBase,
    ProofContextBindingEvaluatorBase,
)
from tigrbl_proof_of_possession_contracts import (
    ConfirmationKeyResolverPort,
    PossessionProofIssuerPort,
    PossessionProofVerifierPort,
    ProofContextBindingEvaluatorPort,
)
from tigrbl_protected_envelope_bases import (
    ProtectedEnvelopeIssuerBase,
    ProtectedEnvelopeVerifierBase,
)
from tigrbl_token_bases import ProfiledTokenIssuerBase, ProfiledTokenVerifierBase
from tigrbl_workload_identity_bases import (
    DelegatedWorkloadCredentialProviderBase,
    WorkloadCredentialProviderBase,
    WorkloadCredentialVerifierBase,
    WorkloadReferenceResolverBase,
    WorkloadTrustMaterialProviderBase,
)
from tigrbl_workload_identity_contracts import (
    DelegatedWorkloadCredentialProviderPort,
    WorkloadCredentialProviderPort,
    WorkloadCredentialVerifierPort,
    WorkloadReferenceResolverPort,
    WorkloadTrustMaterialProviderPort,
)


def test_identity_document_bases_implement_canonical_ports() -> None:
    assert IdentityDocumentResolverPort in IdentityDocumentResolverBase.__mro__
    assert IdentityDocumentPublisherPort in IdentityDocumentPublisherBase.__mro__
    assert IdentityDocumentVerifierPort in IdentityDocumentVerifierBase.__mro__


def test_proof_bases_implement_canonical_ports() -> None:
    assert PossessionProofIssuerPort in PossessionProofIssuerBase.__mro__
    assert PossessionProofVerifierPort in PossessionProofVerifierBase.__mro__
    assert ConfirmationKeyResolverPort in ConfirmationKeyResolverBase.__mro__
    assert ProofContextBindingEvaluatorPort in ProofContextBindingEvaluatorBase.__mro__


def test_workload_bases_are_protocol_neutral() -> None:
    pairs = (
        (WorkloadReferenceResolverBase, WorkloadReferenceResolverPort),
        (WorkloadCredentialProviderBase, WorkloadCredentialProviderPort),
        (
            DelegatedWorkloadCredentialProviderBase,
            DelegatedWorkloadCredentialProviderPort,
        ),
        (WorkloadCredentialVerifierBase, WorkloadCredentialVerifierPort),
        (WorkloadTrustMaterialProviderBase, WorkloadTrustMaterialProviderPort),
    )
    for base, port in pairs:
        assert port in base.__mro__
        assert "spiffe" not in base.__name__.lower()
        assert "svid" not in base.__name__.lower()


def test_jose_and_cose_bases_share_neutral_envelope_and_token_extensions() -> None:
    assert issubclass(JoseEnvelopeIssuerBase, ProtectedEnvelopeIssuerBase)
    assert issubclass(JoseEnvelopeVerifierBase, ProtectedEnvelopeVerifierBase)
    assert issubclass(CoseEnvelopeIssuerBase, ProtectedEnvelopeIssuerBase)
    assert issubclass(CoseEnvelopeVerifierBase, ProtectedEnvelopeVerifierBase)
    assert issubclass(JwtTokenIssuerBase, ProfiledTokenIssuerBase)
    assert issubclass(JwtTokenVerifierBase, ProfiledTokenVerifierBase)
    assert issubclass(CwtTokenIssuerBase, ProfiledTokenIssuerBase)
    assert issubclass(CwtTokenVerifierBase, ProfiledTokenVerifierBase)