from tigrbl_identity_core import ProtectedEnvelopeKind
from tigrbl_protected_envelope_contracts import EnvelopeProtectionRequest, EnvelopeVerificationRequest, ProtectedEnvelope

class JweProtocol:
    def __init__(self, capability, profile): self.capability, self.profile = capability, profile
    def encrypt(self, payload: bytes, *, key_reference: str, headers: dict[str, object]) -> ProtectedEnvelope:
        self.profile.validate_headers(headers)
        return self.capability.protect_envelope(EnvelopeProtectionRequest(ProtectedEnvelopeKind.JWE,payload,headers,key_reference,self.profile.name))
    def decrypt(self, envelope: ProtectedEnvelope):
        self.profile.validate_headers(envelope.protected_headers)
        result=self.capability.verify_envelope(EnvelopeVerificationRequest(envelope,expected_profile=self.profile.name))
        if not result.valid: raise ValueError(result.reason or "JWE decryption failed")
        return result