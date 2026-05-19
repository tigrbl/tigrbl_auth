from __future__ import annotations

from pathlib import Path

from tigrbl_auth.api.rest.schemas import PushedAuthorizationResponse
from tigrbl_auth.framework import Depends, TigrblRouter
from tigrbl_auth.ops.par import pushed_authorization_request
from tigrbl_auth.tables import get_db

api = TigrblRouter()
router = api


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


@api.route('/par', methods=['POST'], response_model=PushedAuthorizationResponse)
async def par(request, db=Depends(get_db)):
    result = await pushed_authorization_request(request=request, db=db)
    from tigrbl_auth.services.session_service import observe_par_response

    payload = result if isinstance(result, dict) else getattr(result, 'model_dump', lambda **_: {})(mode='json')
    observe_par_response(_repo_root(), request_uri=payload.get('request_uri'), details=payload)
    return result
