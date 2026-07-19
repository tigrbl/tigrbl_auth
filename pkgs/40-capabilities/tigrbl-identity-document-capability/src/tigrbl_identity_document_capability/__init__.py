from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import CapabilityDefinition, CapabilityOperation

class IdentityDocumentCapability(Capability):
    def __init__(self,resolver,verifier,publisher=None):
        self._resolver=resolver;self._verifier=verifier;self._publisher=publisher
        super().__init__(CapabilityDefinition("identity-document.processing","1.0"),operations={
            "resolve_identity_document":CapabilityOperation(target=self.resolve_identity_document,delegated=True),
            "verify_identity_document":CapabilityOperation(target=self.verify_identity_document,delegated=True),
            "publish_identity_document":CapabilityOperation(target=self.publish_identity_document if publisher is not None else None,required=False,delegated=True),
        })
    def resolve_identity_document(self,identifier): return self._resolver.resolve(identifier)
    def verify_identity_document(self,request): return self._verifier.verify(request)
    def publish_identity_document(self,document):
        if self._publisher is None: raise LookupError("identity document publisher is not configured")
        return self._publisher.publish(document)
__all__=["IdentityDocumentCapability"]