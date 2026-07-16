"""API-key authentication over injected durable operations."""

from __future__ import annotations

import inspect
from collections.abc import Awaitable, Callable, Mapping
from datetime import datetime, timezone
from typing import TypeAlias

from tigrbl_authenticator_api_key_local import ApiKeyLocalAuthenticator
from tigrbl_capability import Capability
from tigrbl_identity_contracts.authenticators import AuthenticationEvidence
from tigrbl_identity_contracts.capabilities import CapabilityDefinition, CapabilityOperation
from tigrbl_identity_contracts.principal_authentication import RecordAuthenticationResult

KeyLookup: TypeAlias = Callable[[object, str], object | Awaitable[object]]
PrincipalResolver: TypeAlias = Callable[[object, object], object | Awaitable[object]]
CredentialTouch: TypeAlias = Callable[[object, object], object | Awaitable[object]]


async def _resolve(value: object | Awaitable[object]) -> object:
    return await value if inspect.isawaitable(value) else value


def _field(record: object, name: str, default: object = None) -> object:
    return record.get(name, default) if isinstance(record, Mapping) else getattr(record, name, default)


def _valid_key(records: object) -> object | None:
    now = datetime.now(timezone.utc)
    for record in records if isinstance(records, (list, tuple)) else ():
        if _field(record, "status", "active") != "active":
            continue
        valid_from, valid_to = _field(record, "valid_from"), _field(record, "valid_to")
        if isinstance(valid_from, datetime) and valid_from > now or isinstance(valid_to, datetime) and valid_to <= now:
            continue
        return record
    return None


class ApiKeyAuthenticationCapability(Capability):
    def __init__(self, *, find_api_keys: KeyLookup, resolve_user: PrincipalResolver, mark_used: CredentialTouch, authenticator: ApiKeyLocalAuthenticator | None = None) -> None:
        self._find_api_keys, self._resolve_user, self._mark_used = find_api_keys, resolve_user, mark_used
        self._authenticator = authenticator or ApiKeyLocalAuthenticator()
        super().__init__(CapabilityDefinition("principal.authentication.api-key", "1.0"), operations={"authenticate_api_key": CapabilityOperation(target=self.authenticate_api_key, delegated=True)})

    async def authenticate_api_key(self, *, api_key: str, db: object) -> RecordAuthenticationResult:
        credential = _valid_key(await _resolve(self._find_api_keys(db, self._authenticator.digest_key(api_key))))
        if credential is None:
            return RecordAuthenticationResult(False, reason="API key invalid, revoked, or expired")
        principal = await _resolve(self._resolve_user(db, credential))
        if principal is None or not bool(_field(principal, "is_active", True)):
            return RecordAuthenticationResult(False, reason="invalid API key")
        await _resolve(self._mark_used(db, credential))
        return RecordAuthenticationResult(True, record=principal, credential_record=credential, principal_kind="user", evidence=AuthenticationEvidence(authenticator_kind=self._authenticator.kind, credential_kind=self._authenticator.credential_kind, credential_id=str(_field(credential, "id", "")) or None, subject_id=str(_field(principal, "id", "")) or None))


__all__ = ["ApiKeyAuthenticationCapability", "CredentialTouch", "KeyLookup", "PrincipalResolver"]
