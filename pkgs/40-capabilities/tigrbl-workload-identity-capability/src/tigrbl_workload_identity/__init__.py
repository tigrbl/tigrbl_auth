from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import CapabilityDefinition, CapabilityOperation

class WorkloadIdentityCapability(Capability):
    """Protocol-neutral workload credential acquisition and verification."""
    def __init__(self,provider,verifier,trust_material_provider=None,refresher=None):
        self._provider=provider;self._verifier=verifier;self._trust_material_provider=trust_material_provider;self._refresher=refresher
        super().__init__(CapabilityDefinition("workload-identity.credentials","1.0"),operations={
            "obtain_workload_credential":CapabilityOperation(target=self.obtain_workload_credential,delegated=True),
            "verify_workload_credential":CapabilityOperation(target=self.verify_workload_credential,delegated=True),
            "resolve_workload_trust":CapabilityOperation(target=self.resolve_workload_trust if trust_material_provider is not None else None,required=False,delegated=True),
            "refresh_workload_credentials":CapabilityOperation(target=self.refresh_workload_credentials if refresher is not None else None,required=False,delegated=True),
        })
    def obtain_workload_credential(self,request): return self._provider.obtain(request)
    def verify_workload_credential(self,credential,expected_identity=None): return self._verifier.verify(credential,expected_identity)
    def resolve_workload_trust(self,identity,format):
        if self._trust_material_provider is None: raise LookupError("workload trust provider is not configured")
        return self._trust_material_provider.trust_material_for(identity,format)
    def refresh_workload_credentials(self,request):
        if self._refresher is None: raise LookupError("workload credential refresher is not configured")
        return self._refresher(request)
__all__=["WorkloadIdentityCapability"]