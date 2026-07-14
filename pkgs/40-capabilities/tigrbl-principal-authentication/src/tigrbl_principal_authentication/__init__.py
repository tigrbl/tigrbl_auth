"""Composable local principal authentication capabilities."""

from __future__ import annotations

import inspect
from collections.abc import Awaitable, Callable, Mapping
from datetime import datetime, timezone
from typing import Any, TypeAlias

from tigrbl_authenticator_api_key_local import ApiKeyLocalAuthenticator
from tigrbl_authenticator_client_secret_local import ClientSecretLocalAuthenticator
from tigrbl_authenticator_password_local import PasswordLocalAuthenticator
from tigrbl_authenticator_service_key_local import ServiceKeyLocalAuthenticator
from tigrbl_capability import Capability
from tigrbl_identity_contracts.authenticators import AuthenticationEvidence
from tigrbl_identity_contracts.capabilities import CapabilityDefinition, CapabilityOperation
from tigrbl_identity_contracts.principal_authentication import RecordAuthenticationResult


RecordLookup: TypeAlias = Callable[[Mapping[str, Any]], object | Awaitable[object]]
KeyLookup: TypeAlias = Callable[[object, str], object | Awaitable[object]]
PrincipalResolver: TypeAlias = Callable[[object, object], object | Awaitable[object]]
CredentialTouch: TypeAlias = Callable[[object, object], object | Awaitable[object]]


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
        if (
            record is None
            or not bool(_field(record, "is_active", True))
            or not self._authenticator.verify_secret(password, encoded)
        ):
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


class ApiKeyAuthenticationCapability(Capability):
    """Authenticate user API keys and service keys through injected durability."""

    def __init__(
        self,
        *,
        find_api_keys: KeyLookup,
        find_service_keys: KeyLookup,
        resolve_user: PrincipalResolver,
        mark_used: CredentialTouch,
        api_key_authenticator: ApiKeyLocalAuthenticator | None = None,
        service_key_authenticator: ServiceKeyLocalAuthenticator | None = None,
    ) -> None:
        self._find_api_keys = find_api_keys
        self._find_service_keys = find_service_keys
        self._resolve_user = resolve_user
        self._mark_used = mark_used
        self._api_key_authenticator = api_key_authenticator or ApiKeyLocalAuthenticator()
        self._service_key_authenticator = service_key_authenticator or ServiceKeyLocalAuthenticator()
        super().__init__(
            CapabilityDefinition("principal.authentication.api-key", "1.0"),
            operations={
                "authenticate_api_key": CapabilityOperation(
                    target=self.authenticate_api_key,
                    delegated=True,
                ),
            },
        )

    @staticmethod
    def _valid_key(records: object) -> object | None:
        now = datetime.now(timezone.utc)
        for record in records if isinstance(records, (list, tuple)) else ():
            status = _field(record, "status", "active")
            if isinstance(status, str) and status != "active":
                continue
            valid_from = _field(record, "valid_from")
            valid_to = _field(record, "valid_to")
            if isinstance(valid_from, datetime) and valid_from > now:
                continue
            if isinstance(valid_to, datetime) and valid_to <= now:
                continue
            return record
        return None

    @staticmethod
    def _service_principal(record: object) -> object | None:
        return (
            _field(record, "service_identity")
            or _field(record, "_service_identity")
            or _field(record, "service")
            or _field(record, "_service")
        )

    @staticmethod
    def _evidence(
        authenticator: object,
        *,
        principal: object,
        credential: object,
    ) -> AuthenticationEvidence:
        return AuthenticationEvidence(
            authenticator_kind=_field(authenticator, "kind"),
            credential_kind=_field(authenticator, "credential_kind"),
            credential_id=str(_field(credential, "id", "")) or None,
            subject_id=str(_field(principal, "id", "")) or None,
        )

    async def authenticate_api_key(
        self,
        *,
        api_key: str,
        db: object,
    ) -> RecordAuthenticationResult:
        digest = self._api_key_authenticator.digest_key(api_key)
        api_key_record = self._valid_key(
            await _resolve(self._find_api_keys(db, digest))
        )
        if api_key_record is not None:
            principal = await _resolve(self._resolve_user(db, api_key_record))
            if principal is None or not bool(_field(principal, "is_active", True)):
                return RecordAuthenticationResult(False, reason="invalid API key")
            await _resolve(self._mark_used(db, api_key_record))
            return RecordAuthenticationResult(
                True,
                record=principal,
                credential_record=api_key_record,
                principal_kind="user",
                evidence=self._evidence(
                    self._api_key_authenticator,
                    principal=principal,
                    credential=api_key_record,
                ),
            )

        service_key_record = self._valid_key(
            await _resolve(
                self._find_service_keys(
                    db,
                    self._service_key_authenticator.digest_key(api_key),
                )
            )
        )
        if service_key_record is not None:
            principal = self._service_principal(service_key_record)
            if principal is None or not bool(_field(principal, "is_active", True)):
                return RecordAuthenticationResult(False, reason="invalid service key")
            await _resolve(self._mark_used(db, service_key_record))
            return RecordAuthenticationResult(
                True,
                record=principal,
                credential_record=service_key_record,
                principal_kind="service_identity",
                evidence=self._evidence(
                    self._service_key_authenticator,
                    principal=principal,
                    credential=service_key_record,
                ),
            )

        return RecordAuthenticationResult(
            False,
            reason="API key invalid, revoked, or expired",
        )


__all__ = [
    "ApiKeyAuthenticationCapability",
    "ClientSecretAuthenticationCapability",
    "CredentialTouch",
    "KeyLookup",
    "PasswordAuthenticationCapability",
    "PrincipalResolver",
    "RecordLookup",
]
