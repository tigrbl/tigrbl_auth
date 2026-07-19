from tigrbl_identity_core import ProtectedEnvelopeKind
from tigrbl_protected_envelope_contracts import EnvelopeProtectionRequest, EnvelopeVerificationRequest
class CoseProtocol:
    def __init__(self, capability, profile): self.capability,self.profile=capability,profile
    def sign1(self,payload:bytes,*,key_reference:str,headers:dict[object,object],external_aad:bytes=b""):
        self.profile.validate_headers(headers); return self.capability.protect_envelope(EnvelopeProtectionRequest(ProtectedEnvelopeKind.COSE_SIGN1,payload,headers,key_reference,self.profile.name,external_aad))
    def verify1(self,envelope,*,external_aad:bytes=b""):
        self.profile.validate_headers(envelope.protected_headers); result=self.capability.verify_envelope(EnvelopeVerificationRequest(envelope,expected_profile=self.profile.name,external_aad=external_aad))
        if not result.valid: raise ValueError(result.reason or "COSE Sign1 verification failed")
        return result