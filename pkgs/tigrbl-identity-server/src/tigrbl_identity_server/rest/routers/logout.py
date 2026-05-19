from __future__ import annotations

import json
from pathlib import Path

from tigrbl_auth.framework import Depends, TigrblRouter
from tigrbl_auth.ops.logout import logout_request
from tigrbl_auth.tables import get_db

api = TigrblRouter()
router = api


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


@api.route('/logout', methods=['GET', 'POST'], response_model=None)
async def logout(request, db=Depends(get_db)):
    result = await logout_request(request=request, db=db)
    from tigrbl_auth.services.session_service import observe_logout_response

    payload: dict[str, object] = {}
    body = getattr(result, 'body', None)
    if body:
        try:
            payload = json.loads(body.decode('utf-8'))
        except Exception:
            payload = {}
    if not payload:
        headers = getattr(result, 'headers', {}) or {}
        payload = {
            'status': headers.get('x-tigrbl-auth-logout-status'),
            'logout_id': headers.get('x-tigrbl-auth-logout-id'),
            'session_id': headers.get('x-tigrbl-auth-session-id'),
        }
    observe_logout_response(_repo_root(), session_id=payload.get('session_id'), details=payload)
    return result
