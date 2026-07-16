"""Password authentication over injected identity lookup."""

from __future__ import annotations

import inspect
from collections.abc import Awaitable, Callable, Mapping
from typing import Any, TypeAlias

from tigrbl_authenticator_password_local import PasswordLocalAuthenticator
from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import CapabilityDefinition, CapabilityOperation
from tigrbl_identity_contracts.principal_authentication import RecordAuthenticationResult

RecordLookup: TypeAlias = Callable[[Mapping[str, Any]], object | Awaitable[object]]


async def _resolve(value: object | Awaitable[object]) -> object:
    return await value if inspect.isawaitable(value) else value


def _field(record: object, name: str, default: object = None) -> object:
    return record.get(name, default) if isinstance(record, Mapping) else getattr(record, name, default)


class PasswordAuthenticationCapability(Capability):
    def __init__(self, lookup_identity: RecordLookup, authenticator: PasswordLocalAuthenticator | None = None) -> None:
        self._lookup_identity = lookup_identity
        self._authenticator = authenticator or PasswordLocalAuthenticator()
        super().__init__(
            CapabilityDefinition("principal.authentication.password", "1.0"),
            operations={"authenticate_password": CapabilityOperation(target=self.authenticate_password, delegated=True)},
        )

    async def authenticate_password(self, *, identifier: str, password: str | bytes, db: object) -> RecordAuthenticationResult:
        record = await _resolve(self._lookup_identity({"payload": {"identifier": identifier}, "db": db}))
        encoded = _field(record, "password_hash") if record is not None else None
        if record is None or not bool(_field(record, "is_active", True)) or not self._authenticator.verify_secret(password, encoded):
            return RecordAuthenticationResult(False, reason="invalid credentials")
        subject_id = str(_field(record, "id", "")) or None
        return RecordAuthenticationResult(True, record=record, evidence=self._authenticator.evidence(subject_id=subject_id))


__all__ = ["PasswordAuthenticationCapability", "RecordLookup"]
