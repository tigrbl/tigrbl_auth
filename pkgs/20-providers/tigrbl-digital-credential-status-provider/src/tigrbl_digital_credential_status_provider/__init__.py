from tigrbl_digital_credential_bases import CredentialStatusResolverBase
from tigrbl_identity_contracts.digital_credentials import CredentialStatusReference


class InMemoryCredentialStatusProvider(CredentialStatusResolverBase):
    def __init__(self):
        self._statuses: dict[tuple[str, str, str | int | None], str] = {}

    def publish(self, reference: CredentialStatusReference, status: str) -> None:
        if status not in {"valid", "suspended", "revoked", "unknown"}:
            raise ValueError("unsupported credential lifecycle status")
        self._statuses[(reference.method, reference.uri, reference.index)] = status

    def resolve(self, reference: CredentialStatusReference, /) -> str:
        return self._statuses.get(
            (reference.method, reference.uri, reference.index), "unknown"
        )


__all__ = ["InMemoryCredentialStatusProvider"]
