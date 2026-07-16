"""Client-secret authentication over injected client lookup."""

from __future__ import annotations

import inspect
from collections.abc import Awaitable, Callable, Mapping
from typing import Any, TypeAlias

from tigrbl_authenticator_client_secret_local import ClientSecretLocalAuthenticator
from tigrbl_capability import Capability
from tigrbl_identity_contracts.authenticators import AuthenticationEvidence
from tigrbl_identity_contracts.capabilities import CapabilityDefinition, CapabilityOperation
from tigrbl_identity_contracts.principal_authentication import RecordAuthenticationResult

RecordLookup: TypeAlias = Callable[[Mapping[str, Any]], object | Awaitable[object]]


async def _resolve(value: object | Awaitable[object]) -> object:
    return await value if inspect.isawaitable(value) else value


def _field(record: object, name: str, default: object = None) -> object:
    return record.get(name, default) if isinstance(record, Mapping) else getattr(record, name, default)


class ClientSecretAuthenticationCapability(Capability):
    def __init__(self, lookup_client: RecordLookup, authenticator: ClientSecretLocalAuthenticator | None = None) -> None:
        self._lookup_client = lookup_client
        self._authenticator = authenticator or ClientSecretLocalAuthenticator()
        super().__init__(
            CapabilityDefinition("principal.authentication.client-secret", "1.0"),
            operations={
                "authenticate_client_secret": CapabilityOperation(target=self.authenticate_client_secret, delegated=True),
                "verify_client_record": CapabilityOperation(target=self.verify_client_record, delegated=True),
            },
        )

    def verify_client_record(self, record: object, presented_secret: str | bytes) -> RecordAuthenticationResult:
        if not bool(_field(record, "is_active", True)) or not self._authenticator.verify_secret(presented_secret, _field(record, "client_secret_hash")):
            return RecordAuthenticationResult(False, reason="invalid client")
        subject_id = str(_field(record, "id", "")) or None
        return RecordAuthenticationResult(True, record=record, evidence=AuthenticationEvidence(authenticator_kind=self._authenticator.kind, credential_kind=self._authenticator.credential_kind, subject_id=subject_id))

    async def authenticate_client_secret(self, *, client_id: str, client_secret: str | bytes, db: object) -> RecordAuthenticationResult:
        record = await _resolve(self._lookup_client({"payload": {"client_id": client_id}, "db": db}))
        return RecordAuthenticationResult(False, reason="invalid client") if record is None else self.verify_client_record(record, client_secret)


__all__ = ["ClientSecretAuthenticationCapability", "RecordLookup"]
