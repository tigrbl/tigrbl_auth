"""Current-subject authentication-session HTTP routes."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel
from tigrbl import TigrblRouter
from tigrbl.requests import Request
from tigrbl.runtime.status import HTTPException
from tigrbl.security import Depends
from tigrbl_identity_contracts.account_self_service import (
    AccountNotFoundError,
    AccountPrincipal,
    AccountSession,
)
from tigrbl_identity_server.account_self_service import (
    account_principal,
    account_self_service_for_request,
    get_db,
)

from .common import MyAccountMutationOut, current_principal_dependency


class MyAccountSessionOut(BaseModel):
    id: str
    tenant_id: str
    user_id: str
    username: str
    client_id: str | None = None
    state: str = "active"
    auth_time: str | None = None
    last_seen_at: str | None = None
    expires_at: str | None = None
    ended_at: str | None = None


def _session_payload(session: AccountSession) -> MyAccountSessionOut:
    return MyAccountSessionOut(
        id=session.session_id,
        tenant_id=session.tenant_id,
        user_id=session.identity_id,
        username=session.username,
        client_id=session.client_id,
        state=session.state,
        auth_time=session.auth_time,
        last_seen_at=session.last_seen_at,
        expires_at=session.expires_at,
        ended_at=session.ended_at,
    )


api = router = TigrblRouter()
MY_ACCOUNT_TAGS = ["My Account"]


@api.route(
    "/account/sessions",
    methods=["GET"],
    response_model=list[MyAccountSessionOut],
    tags=MY_ACCOUNT_TAGS,
)
async def list_account_sessions(
    request: Request | None = None,
    current_user: AccountPrincipal | object = Depends(current_principal_dependency),
    db: Any = Depends(get_db),
) -> list[MyAccountSessionOut]:
    principal = account_principal(current_user)
    sessions = await account_self_service_for_request(
        request or object(), db
    ).list_sessions(principal)
    return [_session_payload(session) for session in sessions]


@api.route(
    "/account/sessions/{session_id}",
    methods=["DELETE"],
    response_model=MyAccountMutationOut,
    tags=MY_ACCOUNT_TAGS,
)
async def revoke_account_session(
    session_id: str,
    request: Request | None = None,
    current_user: AccountPrincipal | object = Depends(current_principal_dependency),
    db: Any = Depends(get_db),
) -> MyAccountMutationOut:
    try:
        result = await account_self_service_for_request(
            request or object(), db
        ).revoke_session(account_principal(current_user), session_id)
    except AccountNotFoundError as exc:
        raise HTTPException(404, str(exc)) from exc
    return MyAccountMutationOut(status=result.status, id=result.resource_id)


__all__ = [
    "MyAccountSessionOut",
    "api",
    "list_account_sessions",
    "revoke_account_session",
    "router",
]
