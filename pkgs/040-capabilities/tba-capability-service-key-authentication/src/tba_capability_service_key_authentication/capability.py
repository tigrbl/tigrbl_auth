"""Service-key authentication over injected durable operations."""

from __future__ import annotations

from tba_capability_api_key_authentication.capability import CredentialTouch, KeyLookup, _field, _resolve, _valid_key
from tba_provider_authenticator_service_key_local import ServiceKeyLocalAuthenticator
from tba_concrete_capability import Capability
from tba_contracts_identity.authenticators import AuthenticationEvidence
from tba_contracts_identity.capabilities import CapabilityDefinition, CapabilityOperation
from tba_contracts_identity.principal_authentication import RecordAuthenticationResult


class ServiceKeyAuthenticationCapability(Capability):
    def __init__(self, *, find_service_keys: KeyLookup, mark_used: CredentialTouch, authenticator: ServiceKeyLocalAuthenticator | None = None) -> None:
        self._find_service_keys, self._mark_used = find_service_keys, mark_used
        self._authenticator = authenticator or ServiceKeyLocalAuthenticator()
        super().__init__(CapabilityDefinition("principal.authentication.service-key", "1.0"), operations={"authenticate_service_key": CapabilityOperation(target=self.authenticate_service_key, delegated=True)})

    @staticmethod
    def _service_principal(record: object) -> object | None:
        return _field(record, "service_identity") or _field(record, "_service_identity") or _field(record, "service") or _field(record, "_service")

    async def authenticate_service_key(self, *, service_key: str, db: object) -> RecordAuthenticationResult:
        credential = _valid_key(await _resolve(self._find_service_keys(db, self._authenticator.digest_key(service_key))))
        if credential is None:
            return RecordAuthenticationResult(False, reason="service key invalid, revoked, or expired")
        principal = self._service_principal(credential)
        if principal is None or not bool(_field(principal, "is_active", True)):
            return RecordAuthenticationResult(False, reason="invalid service key")
        await _resolve(self._mark_used(db, credential))
        return RecordAuthenticationResult(True, record=principal, credential_record=credential, principal_kind="service_identity", evidence=AuthenticationEvidence(authenticator_kind=self._authenticator.kind, credential_kind=self._authenticator.credential_kind, credential_id=str(_field(credential, "id", "")) or None, subject_id=str(_field(principal, "id", "")) or None))


__all__ = ["ServiceKeyAuthenticationCapability"]
