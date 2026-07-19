from tigrbl_protected_envelope_contracts import EnvelopeVerificationResult, VerificationKeyRequest, VerificationKeyResult
from tigrbl_identity_document_contracts import IdentityDocumentVerificationResult
from tigrbl_proof_of_possession_contracts import PossessionProofVerificationResult

def test_verification_results_distinguish_security_dimensions() -> None:
    result = EnvelopeVerificationResult(True, structural_valid=True, cryptographic_valid=True, key_resolved=True, issuer_trusted=True, profile_valid=True)
    assert result.valid and result.cryptographic_valid and result.issuer_trusted
    assert VerificationKeyRequest("kid", "ES256", profile="vc+jwt").profile == "vc+jwt"
    assert VerificationKeyResult(True, key=object(), trusted=True).trusted
    assert IdentityDocumentVerificationResult(True, structural_valid=True, controller_authorized=True).controller_authorized
    assert PossessionProofVerificationResult(True, replay_accepted=True).replay_accepted is True