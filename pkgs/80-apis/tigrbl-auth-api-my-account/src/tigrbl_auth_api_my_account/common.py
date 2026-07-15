"""Shared HTTP concerns for the My Account API product."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel
from tigrbl.requests import Request
from tigrbl.security import Depends
from tigrbl_identity_contracts.account_self_service import AccountPrincipal
from tigrbl_identity_server.account_self_service import (
    current_account_principal,
    get_db,
)


class MyAccountMutationOut(BaseModel):
    status: str
    id: str | None = None


async def current_principal_dependency(
    request: Request,
    authorization: str | None = None,
    api_key: str | None = None,
    dpop: str | None = None,
    db: Any = Depends(get_db),
) -> AccountPrincipal:
    headers = getattr(request, "headers", {})
    authorization = (
        authorization
        or headers.get("Authorization", "")
        or headers.get("authorization", "")
    )
    api_key = api_key or headers.get("x-api-key")
    dpop = dpop or headers.get("DPoP") or headers.get("dpop")
    return await current_account_principal(
        request,
        authorization=authorization,
        api_key=api_key,
        dpop=dpop,
        db=db,
    )


__all__ = [
    "MyAccountMutationOut",
    "current_principal_dependency",
]
