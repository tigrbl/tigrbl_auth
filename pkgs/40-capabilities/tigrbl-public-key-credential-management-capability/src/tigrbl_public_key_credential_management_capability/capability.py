from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import (
    CapabilityDefinition,
    CapabilityOperation,
    CapabilityState,
)

from .operations import ListCredentials, RenameCredential, RevokeCredential


class PublicKeyCredentialManagementCapability(Capability):
    def __init__(
        self,
        *,
        list_credentials: ListCredentials | None,
        rename_credential: RenameCredential | None,
        revoke_credential: RevokeCredential | None,
    ) -> None:
        ready = all(
            target is not None
            for target in (list_credentials, rename_credential, revoke_credential)
        )
        super().__init__(
            CapabilityDefinition("credential.public-key.management", "1.0"),
            operations={
                "list_public_key_credentials": CapabilityOperation(
                    target=list_credentials, delegated=True
                ),
                "rename_public_key_credential": CapabilityOperation(
                    target=rename_credential, delegated=True
                ),
                "revoke_public_key_credential": CapabilityOperation(
                    target=revoke_credential, delegated=True
                ),
            },
            state=lambda: CapabilityState(
                ready=ready, status="ready" if ready else "unbound"
            ),
        )


__all__ = ["PublicKeyCredentialManagementCapability"]
