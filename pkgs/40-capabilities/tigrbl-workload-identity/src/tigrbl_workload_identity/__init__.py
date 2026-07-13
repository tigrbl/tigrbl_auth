from tigrbl_identity_contracts.workloads import (
    SpiffeId,
    SvidProviderPort,
    SvidVerifierPort,
)


class WorkloadIdentityCapability:
    def __init__(self, provider: SvidProviderPort, verifier: SvidVerifierPort):
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
