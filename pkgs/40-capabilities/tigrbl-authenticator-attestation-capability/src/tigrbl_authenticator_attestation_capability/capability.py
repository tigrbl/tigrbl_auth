from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import (
    CapabilityDefinition,
    CapabilityOperation,
    CapabilityState,
)

from .operations import (
    AppraiseAttestation,
    ReappraiseAuthenticator,
    ResolveAuthenticatorMetadata,
)


class AuthenticatorAttestationCapability(Capability):
    def __init__(
        self,
        *,
        appraise: AppraiseAttestation | None,
        resolve_metadata: ResolveAuthenticatorMetadata | None = None,
        reappraise: ReappraiseAuthenticator | None = None,
    ) -> None:
        super().__init__(
            CapabilityDefinition("authenticator.attestation", "1.0"),
            operations={
                "appraise_authenticator_attestation": CapabilityOperation(
                    target=appraise, delegated=True
                ),
                "resolve_authenticator_metadata": CapabilityOperation(
                    target=resolve_metadata, required=False, delegated=True
                ),
                "reappraise_registered_authenticator": CapabilityOperation(
                    target=reappraise, required=False, delegated=True
                ),
            },
            state=lambda: CapabilityState(
                ready=appraise is not None, status="ready" if appraise else "unbound"
            ),
        )


__all__ = ["AuthenticatorAttestationCapability"]
