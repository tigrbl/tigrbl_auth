from tigrbl_proof_of_possession_contracts import PossessionProofVerificationRequest
from .validation import validate_cwt_svid_extension


class CwtSvidExtensionVerifier:
    def __init__(self, cwt_protocol, proof_verifier):
        self.cwt_protocol, self.proof_verifier = cwt_protocol, proof_verifier

    def verify(self, envelope, *, proof_request: PossessionProofVerificationRequest):
        claims, envelope_result = self.cwt_protocol.verify(envelope)
        proof_result = self.proof_verifier.verify(proof_request)
        validate_cwt_svid_extension(
            envelope.protected_headers, claims.claims, proof_result=proof_result
        )
        return str(claims.claims[2]), envelope_result, proof_result
