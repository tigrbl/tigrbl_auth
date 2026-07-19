from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import CapabilityDefinition, CapabilityOperation

class WorkloadCredentialBrokeringCapability(Capability):
    def __init__(self,reference_resolver,authorization_evaluator,credential_provider,trust_material_provider,credential_watcher=None):
        self._reference_resolver=reference_resolver;self._authorization_evaluator=authorization_evaluator;self._credential_provider=credential_provider;self._trust_material_provider=trust_material_provider;self._credential_watcher=credential_watcher
        super().__init__(CapabilityDefinition("workload-credential.brokering","1.0"),operations={
            "resolve_workload_reference":CapabilityOperation(target=self.resolve_workload_reference,delegated=True),
            "authorize_delegated_credential_access":CapabilityOperation(target=self.authorize_delegated_credential_access,delegated=True),
            "obtain_delegated_workload_credentials":CapabilityOperation(target=self.obtain_delegated_workload_credentials,delegated=True),
            "resolve_delegated_workload_trust":CapabilityOperation(target=self.resolve_delegated_workload_trust,delegated=True),
            "watch_delegated_workload_credentials":CapabilityOperation(target=self.watch_delegated_workload_credentials if credential_watcher is not None else None,required=False,delegated=True),
        })
    def resolve_workload_reference(self,reference): return self._reference_resolver.resolve(reference)
    def authorize_delegated_credential_access(self,request): return self._authorization_evaluator(request)
    def obtain_delegated_workload_credentials(self,request): return self._credential_provider.obtain_for(request)
    def resolve_delegated_workload_trust(self,identity,format): return self._trust_material_provider.trust_material_for(identity,format)
    def watch_delegated_workload_credentials(self,request):
        if self._credential_watcher is None: raise LookupError("credential watcher is not configured")
        return self._credential_watcher(request)
__all__=["WorkloadCredentialBrokeringCapability"]