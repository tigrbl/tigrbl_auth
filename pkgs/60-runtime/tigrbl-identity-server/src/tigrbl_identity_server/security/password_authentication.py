"""Layer-60 composition of password authentication capability."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_contracts.principals import PrincipalLike
from tigrbl_identity_storage_runtime.ops.identities import (
    lookup_identity_by_identifier,
)
from tigrbl_principal_authentication import PasswordAuthenticationCapability


password_authentication = PasswordAuthenticationCapability(
    lookup_identity_by_identifier
)


async def authenticate_password(
    identifier: str,
    password: str,
    db: Any,
) -> PrincipalLike | None:
    result = await password_authentication.authenticate_password(
        identifier=identifier,
        password=password,
        db=db,
    )
    return result.record if result.authenticated else None


__all__ = ["authenticate_password", "password_authentication"]
