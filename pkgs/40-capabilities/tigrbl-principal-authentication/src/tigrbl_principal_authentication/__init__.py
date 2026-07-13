"""Composable local principal authentication capabilities."""

from __future__ import annotations

import inspect
from collections.abc import Awaitable, Callable, Mapping
from typing import Any, TypeAlias

from tigrbl_authenticator_client_secret_local import ClientSecretLocalAuthenticator
from tigrbl_authenticator_password_local import PasswordLocalAuthenticator
from tigrbl_capability import Capability
from tigrbl_identity_contracts.authenticators import AuthenticationEvidence
from tigrbl_identity_contracts.capabilities import CapabilityDefinition, CapabilityOperation
from tigrbl_identity_contracts.principal_authentication import RecordAuthenticationResult


RecordLookup: TypeAlias = Callable[[Mapping[str, Any]], object | Awaitable[object]]


async def _resolve(value: object | Awaitable[object]) -> object:
    return await value if inspect.isawaitable(value) else value


def _field(record: object, name: str, default: object = None) -> object:
    if isinstance(record, Mapping):
        return record.get(name, default)
    return getattr(record, name, default)


class PasswordAuthenticationCapability(Capability):
    def __init__(
        self,
        lookup_identity: RecordLookup,
        authenticator: PasswordLocalAuthenticator | None = None,
    ) -> None:
        self._lookup_identity = lookup_identity
        self._authenticator = authenticator or PasswordLocalAuthenticator()
        super().__init__(
            CapabilityDefinition("principal.authentication.password", "1.0"),
            operations={
                "authenticate_password": CapabilityOperation(
                    target=self.authenticate_password,
                    delegated=True,
                ),
            },
        )

    async def authenticate_password(
        self,
        *,
        identifier: str,
        password: str | bytes,
        db: object,
    ) -> RecordAuthenticationResult:
        record = await _resolve(
            self._lookup_identity({"payload": {"identifier": identifier}, "db": db})
        )
        encoded = _field(record, "password_hash") if record is not None else None
        if record is None or not self._authenticator.verify_secret(password, encoded):
            return RecordAuthenticationResult(False, reason="invalid credentials")
        subject_id = str(_field(record, "id", "")) or None
        return RecordAuthenticationResult(
            True,
            record=record,
            evidence=self._authenticator.evidence(subject_id=subject_id),
        )


class ClientSecretAuthenticationCapability(Capability):
    def __init__(
        self,
        lookup_client: RecordLookup,
        authenticator: ClientSecretLocalAuthenticator | None = None,
    ) -> None:
        self._lookup_client = lookup_client
        self._authenticator = authenticator or ClientSecretLocalAuthenticator()
        super().__init__(
            CapabilityDefinition("principal.authentication.client-secret", "1.0"),
            operations={
                "authenticate_client_secret": CapabilityOperation(
                    target=self.authenticate_client_secret,
                    delegated=True,
                ),
                "verify_client_record": CapabilityOperation(
                    target=self.verify_client_record,
                    delegated=True,
                ),
            },
        )

    def verify_client_record(
        self,
        record: object,
        presented_secret: str | bytes,
    ) -> RecordAuthenticationResult:
        if not bool(_field(record, "is_active", True)):
            return RecordAuthenticationResult(False, reason="invalid client")
        encoded = _field(record, "client_secret_hash")
        if not self._authenticator.verify_secret(presented_secret, encoded):
            return RecordAuthenticationResult(False, reason="invalid client")
        subject_id = str(_field(record, "id", "")) or None
        return RecordAuthenticationResult(
            True,
            record=record,
            evidence=AuthenticationEvidence(
                authenticator_kind=self._authenticator.kind,
                credential_kind=self._authenticator.credential_kind,
                subject_id=subject_id,
            ),
        )

    async def authenticate_client_secret(
        self,
        *,
        client_id: str,
        client_secret: str | bytes,
        db: object,
    ) -> RecordAuthenticationResult:
        record = await _resolve(
            self._lookup_client({"payload": {"client_id": client_id}, "db": db})
        )
        if record is None:
            return RecordAuthenticationResult(False, reason="invalid client")
        return self.verify_client_record(record, client_secret)


__all__ = [
    "ClientSecretAuthenticationCapability",
    "PasswordAuthenticationCapability",
    "RecordLookup",
]
