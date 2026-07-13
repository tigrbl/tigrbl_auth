"""Shared HTTP concerns for the My Account API product."""

from __future__ import annotations

import uuid
from typing import Any

from pydantic import BaseModel
from tigrbl.requests import Request
from tigrbl.runtime.status import HTTPException
from tigrbl.security import Depends
from tigrbl_identity_storage.tables import User
from tigrbl_identity_storage.tables.engine import get_db


class MyAccountMutationOut(BaseModel):
    status: str
    id: str | None = None


def not_found_uuid(value: str, *, field: str) -> uuid.UUID:
    try:
        return uuid.UUID(str(value))
    except ValueError as exc:
        raise HTTPException(404, f"{field} not found") from exc


async def current_principal_dependency(
    request: Request,
    authorization: str | None = None,
    api_key: str | None = None,
    dpop: str | None = None,
    db: Any = Depends(get_db),
) -> User:
    from tigrbl_identity_server.security.auth import get_current_principal

    headers = getattr(request, "headers", {})
    authorization = authorization or headers.get("Authorization", "") or headers.get(
        "authorization", ""
    )
    api_key = api_key or headers.get("x-api-key")
    dpop = dpop or headers.get("DPoP") or headers.get("dpop")
    return await get_current_principal(
        request,
        authorization=authorization,
        api_key=api_key,
        dpop=dpop,
        db=db,
    )


__all__ = [
    "MyAccountMutationOut",
    "current_principal_dependency",
    "not_found_uuid",
]
