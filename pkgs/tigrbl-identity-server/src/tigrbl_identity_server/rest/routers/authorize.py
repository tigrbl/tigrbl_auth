from __future__ import annotations

from typing import Optional

from tigrbl.security import Depends as TigrblDepends
from tigrbl_auth.framework import AsyncSession, Request, TigrblRouter
from tigrbl_auth.ops.authorize import authorize_request
from tigrbl_auth.tables.engine import get_db

api = TigrblRouter()
router = api


@api.route('/authorize', methods=['GET'])
async def authorize(
    request: Request,
    response_type: str | None = None,
    client_id: str | None = None,
    redirect_uri: str | None = None,
    scope: str | None = None,
    response_mode: Optional[str] = None,
    state: Optional[str] = None,
    nonce: Optional[str] = None,
    code_challenge: Optional[str] = None,
    code_challenge_method: Optional[str] = None,
    prompt: Optional[str] = None,
    max_age: Optional[int] = None,
    login_hint: Optional[str] = None,
    claims: Optional[str] = None,
    request_uri: Optional[str] = None,
    request_object: Optional[str] = None,
    authorization_details: Optional[str] = None,
    db: AsyncSession = TigrblDepends(get_db),
):
    params = {
        'response_type': response_type or request.query_params.get('response_type'),
        'client_id': client_id or request.query_params.get('client_id'),
        'redirect_uri': redirect_uri or request.query_params.get('redirect_uri'),
        'scope': scope or request.query_params.get('scope'),
        'response_mode': response_mode or request.query_params.get('response_mode'),
        'state': state or request.query_params.get('state'),
        'nonce': nonce or request.query_params.get('nonce'),
        'code_challenge': code_challenge or request.query_params.get('code_challenge'),
        'code_challenge_method': code_challenge_method or request.query_params.get('code_challenge_method'),
        'prompt': prompt or request.query_params.get('prompt'),
        'max_age': max_age if max_age is not None else request.query_params.get('max_age'),
        'login_hint': login_hint or request.query_params.get('login_hint'),
        'claims': claims or request.query_params.get('claims'),
        'request_uri': request_uri or request.query_params.get('request_uri'),
        'request': request_object or request.query_params.get('request'),
        'authorization_details': authorization_details or request.query_params.get('authorization_details'),
        'resource': list(request.query_params.getlist('resource')) if hasattr(request.query_params, 'getlist') else None,
    }
    return await authorize_request(request=request, db=db, params=params)


__all__ = ['router', 'api']
