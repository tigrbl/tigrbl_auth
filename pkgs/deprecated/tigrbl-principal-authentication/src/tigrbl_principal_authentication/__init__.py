"""Deprecated aggregate imports for principal authentication capabilities."""

from __future__ import annotations

from tigrbl_api_key_authentication_capability import (
    ApiKeyAuthenticationCapability as UserApiKeyAuthenticationCapability,
    CredentialTouch,
    KeyLookup,
    PrincipalResolver,
)
from tigrbl_authenticator_api_key_local import ApiKeyLocalAuthenticator
from tigrbl_authenticator_service_key_local import ServiceKeyLocalAuthenticator
from tigrbl_capability import Capability
from tigrbl_client_secret_authentication_capability import (
    ClientSecretAuthenticationCapability,
)
from tigrbl_identity_contracts.capabilities import CapabilityDefinition, CapabilityOperation
from tigrbl_password_authentication_capability import PasswordAuthenticationCapability, RecordLookup
from tigrbl_service_key_authentication_capability import ServiceKeyAuthenticationCapability

from .backends import ApiKeyBackend, AuthError, PasswordBackend
from .lifecycle import *
from .lifecycle import __all__ as _lifecycle_exports
from .proof_bindings import *
from .proof_bindings import __all__ as _proof_binding_exports


class ApiKeyAuthenticationCapability(Capability):
    """One-release adapter for the former combined API/service-key operation."""

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
        self.user_api_keys = UserApiKeyAuthenticationCapability(
            find_api_keys=find_api_keys,
            resolve_user=resolve_user,
            mark_used=mark_used,
            authenticator=api_key_authenticator,
        )
        self.service_keys = ServiceKeyAuthenticationCapability(
            find_service_keys=find_service_keys,
            mark_used=mark_used,
            authenticator=service_key_authenticator,
        )
        super().__init__(
            CapabilityDefinition("principal.authentication.api-key.compatibility", "1.0"),
            operations={
                "authenticate_api_key": CapabilityOperation(
                    target=self.authenticate_api_key,
                    delegated=True,
                )
            },
        )

    async def authenticate_api_key(self, *, api_key: str, db: object):
        result = await self.user_api_keys.authenticate_api_key(api_key=api_key, db=db)
        if result.authenticated:
            return result
        return await self.service_keys.authenticate_service_key(service_key=api_key, db=db)


__all__ = [
    "ApiKeyAuthenticationCapability",
    "ApiKeyBackend",
    "AuthError",
    "ClientSecretAuthenticationCapability",
    "CredentialTouch",
    "KeyLookup",
    "PasswordAuthenticationCapability",
    "PasswordBackend",
    "PrincipalResolver",
    "RecordLookup",
    "ServiceKeyAuthenticationCapability",
    "UserApiKeyAuthenticationCapability",
    *_lifecycle_exports,
    *_proof_binding_exports,
]
