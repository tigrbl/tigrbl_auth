from tba_bases_cose import (
    CoseEnvelopeIssuerBase,
    CoseEnvelopeVerifierBase,
    CwtTokenIssuerBase,
    CwtTokenVerifierBase,
)
from tba_bases_identity_document import (
    IdentityDocumentPublisherBase,
    IdentityDocumentResolverBase,
    IdentityDocumentVerifierBase,
)
from tba_contracts_identity_document import (
    IdentityDocumentPublisherPort,
    IdentityDocumentResolverPort,
    IdentityDocumentVerifierPort,
)
from tba_bases_jose import (
    JoseEnvelopeIssuerBase,
    JoseEnvelopeVerifierBase,
    JwtTokenIssuerBase,
    JwtTokenVerifierBase,
)
from tba_bases_proof_of_possession import (
    ConfirmationKeyResolverBase,
    PossessionProofIssuerBase,
    PossessionProofVerifierBase,
    ProofContextBindingEvaluatorBase,
)
from tba_contracts_proof_of_possession import (
    ConfirmationKeyResolverPort,
    PossessionProofIssuerPort,
    PossessionProofVerifierPort,
    ProofContextBindingEvaluatorPort,
)
from tba_bases_protected_envelope import (
    ProtectedEnvelopeIssuerBase,
    ProtectedEnvelopeVerifierBase,
)
from tba_bases_token import ProfiledTokenIssuerBase, ProfiledTokenVerifierBase
from tba_bases_workload_identity import (
    DelegatedWorkloadCredentialProviderBase,
    WorkloadCredentialProviderBase,
    WorkloadCredentialVerifierBase,
    WorkloadReferenceResolverBase,
    WorkloadTrustMaterialProviderBase,
)
from tba_contracts_workload_identity import (
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