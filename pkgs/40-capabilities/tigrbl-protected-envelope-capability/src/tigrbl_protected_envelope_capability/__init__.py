from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import CapabilityDefinition, CapabilityOperation

class ProtectedEnvelopeCapability(Capability):
    def __init__(self,issuer,verifier):
        self._issuer=issuer;self._verifier=verifier
        super().__init__(CapabilityDefinition("protected-envelope.processing","1.0"),operations={
            "protect_envelope":CapabilityOperation(target=self.protect_envelope,delegated=True),
            "verify_envelope":CapabilityOperation(target=self.verify_envelope,delegated=True),
        })
    def protect_envelope(self,request): return self._issuer.protect(request)
    def verify_envelope(self,request): return self._verifier.verify(request)
__all__=["ProtectedEnvelopeCapability"]