from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import CapabilityDefinition, CapabilityOperation
from tigrbl_identity_contracts.workloads import (
    SpiffeId,
    SpiffeTrustBundle,
    SvidProviderPort,
    SvidVerifierPort,
    TrustBundleProviderPort,
    TrustDomain,
)


class WorkloadIdentityCapability(Capability):
    def __init__(
        self,
        provider: SvidProviderPort,
        verifier: SvidVerifierPort,
        bundle_provider: TrustBundleProviderPort | None = None,
        refresher=None,
    ):
        super().__init__(
            CapabilityDefinition(
                capability_id="workload-identity.spiffe",
                version="1.0",
            ),
            operations={
                "fetch_x509_svid": CapabilityOperation(
                    target=self.fetch_x509_svid,
                    delegated=True,
                ),
                "fetch_jwt_svid": CapabilityOperation(
                    target=self.fetch_jwt_svid,
                    delegated=True,
                ),
                "verify_svid": CapabilityOperation(
                    target=self.verify_svid,
                    delegated=True,
                ),
                "resolve_bundle": CapabilityOperation(
                    target=self.resolve_bundle if bundle_provider is not None else None,
                    required=False,
                    delegated=True,
                ),
                "refresh": CapabilityOperation(
                    target=self.refresh if refresher is not None else None,
                    required=False,
                    delegated=True,
                ),
            },
        )
        self._provider = provider
        self._verifier = verifier
        self._bundle_provider = bundle_provider
        self._refresher = refresher

    def fetch_x509_svid(self):
        return self._provider.fetch_svid()

    def fetch_jwt_svid(self, audience: str):
        if not audience:
            raise ValueError("JWT-SVID audience is required")
        return self._provider.fetch_svid(audience)

    def verify_svid(self, svid, audience: str | None = None) -> SpiffeId:
        return self._verifier.verify_svid(svid, audience)

    def resolve_bundle(self, trust_domain: TrustDomain) -> SpiffeTrustBundle:
        if self._bundle_provider is None:
            raise LookupError("trust bundle provider is not configured")
        return self._bundle_provider.bundle_for(trust_domain)

    def refresh(self):
        if self._refresher is None:
            raise LookupError("SVID refresh operation is not configured")
        return self._refresher()

    def x509_identity(self) -> SpiffeId:
        return self.verify_svid(self.fetch_x509_svid())

    def jwt_identity(self, audience: str) -> SpiffeId:
        return self.verify_svid(self.fetch_jwt_svid(audience), audience)


__all__ = ["WorkloadIdentityCapability"]
