from __future__ import annotations

from pathlib import Path

from tigrbl.security import Depends as TigrblDepends
from tigrbl_identity_server.framework import AsyncSession, Request, TigrblRouter
from tigrbl_identity_contracts.rest import TokenPair
from tigrbl_identity_oauth.ops.token import token_request
from tigrbl_identity_storage.tables.engine import get_db

api = TigrblRouter()
router = api


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


@api.route('/token', methods=['POST'], response_model=TokenPair)
async def token(request: Request, db: AsyncSession = TigrblDepends(get_db)):
    result = await token_request(request=request, db=db)
    from tigrbl_identity_credentials.session_service import observe_token_response

    payload = result if isinstance(result, dict) else getattr(result, 'model_dump', lambda **_: {})(mode='json')
    observe_token_response(
        _repo_root(),
        access_token=payload.get('access_token'),
        refresh_token=payload.get('refresh_token'),
        id_token=payload.get('id_token'),
        details=payload,
    )
    return result
__all__ = ['router', 'api']
