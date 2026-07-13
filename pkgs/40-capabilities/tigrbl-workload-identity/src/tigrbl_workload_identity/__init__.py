from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import CapabilityDefinition, CapabilityOperation
from tigrbl_identity_contracts.workloads import (
    SpiffeId,
    SvidProviderPort,
    SvidVerifierPort,
)


class WorkloadIdentityCapability(Capability):
    def __init__(self, provider: SvidProviderPort, verifier: SvidVerifierPort):
        super().__init__(
            CapabilityDefinition(
                capability_id="workload-identity.spiffe",
                version="1.0",
            ),
            operations={
                "x509_identity": CapabilityOperation(
                    target=self.x509_identity,
                    delegated=True,
                ),
                "jwt_identity": CapabilityOperation(
                    target=self.jwt_identity,
                    delegated=True,
                ),
            },
        )
        self._provider = provider
        self._verifier = verifier

    def x509_identity(self) -> SpiffeId:
        svid = self._provider.fetch_svid()
        return self._verifier.verify_svid(svid)

    def jwt_identity(self, audience: str) -> SpiffeId:
        if not audience:
            raise ValueError("JWT-SVID audience is required")
        svid = self._provider.fetch_svid(audience)
        return self._verifier.verify_svid(svid, audience)


__all__ = ["WorkloadIdentityCapability"]
