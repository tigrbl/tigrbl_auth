from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import CapabilityDefinition, CapabilityOperation

class PossessionProofCapability(Capability):
    def __init__(self,verifier,key_resolver,context_evaluator,issuer=None):
        self._verifier=verifier;self._key_resolver=key_resolver;self._context_evaluator=context_evaluator;self._issuer=issuer
        super().__init__(CapabilityDefinition("possession-proof.processing","1.0"),operations={
            "verify_possession_proof":CapabilityOperation(target=self.verify_possession_proof,delegated=True),
            "resolve_confirmation_key":CapabilityOperation(target=self.resolve_confirmation_key,delegated=True),
            "evaluate_proof_context":CapabilityOperation(target=self.evaluate_proof_context,delegated=True),
            "issue_possession_proof":CapabilityOperation(target=self.issue_possession_proof if issuer is not None else None,required=False,delegated=True),
        })
    def verify_possession_proof(self,request): return self._verifier.verify(request)
    def resolve_confirmation_key(self,confirmation): return self._key_resolver.resolve_confirmation_key(confirmation)
    def evaluate_proof_context(self,expected,presented): return self._context_evaluator.evaluate_context(expected,presented)
    def issue_possession_proof(self,context):
        if self._issuer is None: raise LookupError("possession proof issuer is not configured")
        return self._issuer.issue(context)
__all__=["PossessionProofCapability"]