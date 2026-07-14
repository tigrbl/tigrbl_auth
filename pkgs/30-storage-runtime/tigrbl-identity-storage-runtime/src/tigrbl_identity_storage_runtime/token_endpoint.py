"""OAuth token endpoint runtime router."""

from __future__ import annotations

from typing import Any

from tigrbl.security import Depends as TigrblDepends
from tigrbl_identity_storage.framework import AsyncSession, Request, TigrblRouter
from .engine import get_db
from tigrbl_identity_storage.tables.token_record import TokenPair
from tigrbl_identity_storage_runtime.token_request import token_request

router = TigrblRouter()


@router.route("/token", methods=["POST"], response_model=TokenPair)
async def token(request: Request, db: AsyncSession = TigrblDepends(get_db)) -> Any:
    return await token_request(request=request, db=db)


__all__ = ["router", "token"]
