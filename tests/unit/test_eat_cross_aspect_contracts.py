from tigrbl_attestation_bases import AttestationAppraiserBase, EvidenceVerifierBase
from tigrbl_cose_bases import EatCwtVerifierBase
from tigrbl_identity_claims_bases import ClaimBase, ClaimSetComposerBase
from tigrbl_identity_contracts.attestation import (
    AttestationEvidence,
    EvidenceVerificationResult,
    VerifiedAttestationEvidence,
)
from tigrbl_identity_contracts.tokens import (
    ProtectedTokenEnvelope,
    TokenEnvelopeFormat,
    TokenProfile,
    VerifiedTokenEnvelope,
)
from tigrbl_jose_bases import EatJwtCoderBase
from tigrbl_token_bases import EatTokenEnvelopeVerifierBase, TokenEnvelopeVerifierBase


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
