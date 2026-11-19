from tba_bases_attestation import AttestationAppraiserBase, EvidenceVerifierBase
from tba_bases_cose import EatCwtVerifierBase
from tba_bases_identity_claims import ClaimBase, ClaimSetComposerBase
from tba_contracts_identity.attestation import (
    AttestationEvidence,
    EvidenceVerificationResult,
    VerifiedAttestationEvidence,
)
from tba_contracts_identity.tokens import (
    ProtectedTokenEnvelope,
    TokenEnvelopeFormat,
    TokenProfile,
    VerifiedTokenEnvelope,
)
from tba_bases_jose import EatJwtCoderBase
from tba_bases_token import EatTokenEnvelopeVerifierBase, TokenEnvelopeVerifierBase


def test_eat_has_distinct_contracts_for_each_cross_cutting_aspect():
    envelope = ProtectedTokenEnvelope(
        "header.payload.signature",
        TokenEnvelopeFormat.JWT,
        TokenProfile.ENTITY_ATTESTATION_TOKEN,
    )
    verified = VerifiedTokenEnvelope(envelope, {"eat_profile": "urn:profile"})
    evidence = AttestationEvidence("urn:profile", verified.claims, envelope.serialized)
    bound = VerifiedAttestationEvidence(evidence, verified)
    result = EvidenceVerificationResult(True, "verified", bound, verified.claims)

    assert result.verified and result.evidence is bound
    assert TokenEnvelopeFormat.CWT.value == "cwt"


def test_eat_has_symmetric_jwt_and_cwt_extension_bases():
    assert issubclass(EatCwtVerifierBase, EatTokenEnvelopeVerifierBase)
    assert issubclass(EatTokenEnvelopeVerifierBase, TokenEnvelopeVerifierBase)
    assert EatJwtCoderBase.__name__ == "EatJwtCoderBase"
    assert ClaimBase.__name__ == "ClaimBase"
    assert ClaimSetComposerBase.__name__ == "ClaimSetComposerBase"
    assert EvidenceVerifierBase.__name__ == "EvidenceVerifierBase"
    assert AttestationAppraiserBase.__name__ == "AttestationAppraiserBase"
