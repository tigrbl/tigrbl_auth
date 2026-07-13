"""Current-subject authentication-session API routes."""

from __future__ import annotations

from http import HTTPStatus
from typing import Any

from pydantic import BaseModel
from tigrbl import TigrblRouter
from tigrbl.runtime.status import HTTPException
from tigrbl.security import Depends
from tigrbl_identity_storage.tables import AuthSession, User
from tigrbl_identity_storage.tables.engine import get_db
from tigrbl_identity_storage_runtime.ops.common import field_value, list_table_records
from tigrbl_identity_storage_runtime.ops.sessions import terminate_session

from .common import (
    MyAccountMutationOut,
    current_principal_dependency,
    not_found_uuid,
)


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


def _iso(value: Any) -> str | None:
    return value.isoformat() if value is not None else None


def _session_payload(session: Any) -> MyAccountSessionOut:
    return MyAccountSessionOut(
        id=str(session.id),
        tenant_id=str(session.tenant_id),
        user_id=str(session.user_id),
        username=str(session.username),
        client_id=str(session.client_id) if session.client_id is not None else None,
        state=str(session.session_state or "active"),
        auth_time=_iso(getattr(session, "auth_time", None)),
        last_seen_at=_iso(getattr(session, "last_seen_at", None)),
        expires_at=_iso(getattr(session, "expires_at", None)),
        ended_at=_iso(getattr(session, "ended_at", None)),
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
    current_user: User = Depends(current_principal_dependency),
    db: Any = Depends(get_db),
) -> list[MyAccountSessionOut]:
    rows = await list_table_records(
        AuthSession,
        db,
        {"user_id": current_user.id, "tenant_id": current_user.tenant_id},
    )
    return [_session_payload(row) for row in rows]


@api.route(
    "/account/sessions/{session_id}",
    methods=["DELETE"],
    response_model=MyAccountMutationOut,
    tags=MY_ACCOUNT_TAGS,
)
async def revoke_account_session(
    session_id: str,
    current_user: User = Depends(current_principal_dependency),
    db: Any = Depends(get_db),
) -> MyAccountMutationOut:
    identifier = not_found_uuid(session_id, field="session")
    rows = await list_table_records(
        AuthSession,
        db,
        {
            "id": identifier,
            "user_id": current_user.id,
            "tenant_id": current_user.tenant_id,
        },
    )
    if not rows:
        raise HTTPException(HTTPStatus.NOT_FOUND, "session not found")
    updated = await terminate_session(
        {
            "path_params": {"id": identifier},
            "payload": {
                "session_id": identifier,
                "session_state": "revoked",
                "reason": "account_self_service",
            },
            "db": db,
        }
    )
    return MyAccountMutationOut(status="revoked", id=str(field_value(updated, "id")))


__all__ = [
    "MyAccountSessionOut",
    "api",
    "list_account_sessions",
    "revoke_account_session",
    "router",
]
