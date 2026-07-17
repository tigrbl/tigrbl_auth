"""Layer-60 composition of split API-key and service-key capabilities."""

from __future__ import annotations

from typing import Any

from tigrbl_api_key_authentication_capability import ApiKeyAuthenticationCapability
from tigrbl_identity_contracts.principals import PrincipalLike
from tigrbl_identity_storage_runtime.ops.authentication_credentials import (
    find_api_keys,
    find_service_keys,
    mark_credential_used,
    resolve_user_principal,
)
from tigrbl_service_key_authentication_capability import ServiceKeyAuthenticationCapability


api_key_authentication = ApiKeyAuthenticationCapability(
    find_api_keys=find_api_keys,
    resolve_user=resolve_user_principal,
    mark_used=mark_credential_used,
)
service_key_authentication = ServiceKeyAuthenticationCapability(
    find_service_keys=find_service_keys,
    mark_used=mark_credential_used,
)


async def authenticate_api_key(raw_key: str, db: Any) -> PrincipalLike | None:
    result = await api_key_authentication.authenticate_api_key(api_key=raw_key, db=db)
    if not result.authenticated:
        result = await service_key_authentication.authenticate_service_key(
            service_key=raw_key,
            db=db,
        )
    return result.record if result.authenticated else None


__all__ = [
    "api_key_authentication",
    "authenticate_api_key",
    "service_key_authentication",
]
