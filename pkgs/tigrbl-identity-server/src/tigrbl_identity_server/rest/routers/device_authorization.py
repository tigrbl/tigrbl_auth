from __future__ import annotations

from pathlib import Path

from tigrbl_identity_contracts.rest import DeviceAuthorizationOut
from tigrbl_identity_server.framework import Depends, TigrblRouter
from tigrbl_auth_protocol_oauth.ops.device_authorization import device_authorization_request
from tigrbl_identity_storage.tables import get_db

api = TigrblRouter()
router = api


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


@api.route('/device_authorization', methods=['POST'], response_model=DeviceAuthorizationOut)
async def device_authorization(request, db=Depends(get_db)):
    result = await device_authorization_request(request=request, db=db)
    from tigrbl_authn_credentials.session_service import observe_device_authorization_response

    payload = result if isinstance(result, dict) else getattr(result, 'model_dump', lambda **_: {})(mode='json')
    observe_device_authorization_response(_repo_root(), device_code=payload.get('device_code'), details=payload)
    return result
