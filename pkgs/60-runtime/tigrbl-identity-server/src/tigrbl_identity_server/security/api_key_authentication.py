"""Layer-60 composition of API/service-key authentication capability."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_contracts.principals import PrincipalLike
from tigrbl_identity_storage_runtime.ops.authentication_credentials import (
    digest_api_key,
    find_api_keys,
    find_service_keys,
    mark_credential_used,
    resolve_user_principal,
)
from tigrbl_principal_authentication import ApiKeyAuthenticationCapability


api_key_authentication = ApiKeyAuthenticationCapability(
    digest_key=digest_api_key,
    find_api_keys=find_api_keys,
    find_service_keys=find_service_keys,
    resolve_user=resolve_user_principal,
    mark_used=mark_credential_used,
)


async def authenticate_api_key(
    raw_key: str,
    db: Any,
) -> PrincipalLike | None:
    result = await api_key_authentication.authenticate_api_key(
        api_key=raw_key,
        db=db,
    )
    return result.record if result.authenticated else None


__all__ = ["api_key_authentication", "authenticate_api_key"]
