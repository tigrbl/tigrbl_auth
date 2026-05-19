from __future__ import annotations

from tigrbl.security import Depends as TigrblDepends
from tigrbl_auth.framework import AsyncSession, Request, TigrblRouter
from tigrbl_auth.tables.engine import get_db
from tigrbl_auth.api.rest.schemas import CredsIn, TokenPair
from tigrbl_auth.ops.login import login_user

api = TigrblRouter()
router = api


@api.route('/login', methods=['POST'], response_model=TokenPair)
async def login(request: Request, creds: CredsIn | None = None, db: AsyncSession = TigrblDepends(get_db)):
    if creds is None:
        body = await request.json() or {}
        creds = CredsIn.model_validate(body)
    return await login_user(request=request, db=db, identifier=creds.identifier, password=creds.password)


__all__ = ['router', 'api']
