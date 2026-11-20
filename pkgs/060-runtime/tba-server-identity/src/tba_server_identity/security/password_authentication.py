"""Layer-60 composition of password authentication capability."""

from __future__ import annotations

from typing import Any

from tba_contracts_identity.principals import PrincipalLike
from tba_runtime_identity_storage.ops.identities import (
    lookup_identity_by_identifier,
)
from tba_capability_password_authentication import PasswordAuthenticationCapability


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
