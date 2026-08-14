"""Runtime composition for the interactive session-login HTTP carrier."""

from tigrbl_auth_router_session_login import build_login_router
from tigrbl_identity_storage_runtime.engine import get_db

from tigrbl_identity_server.login_runtime import (
    change_required_password,
    login_user,
    password_authentication,
)


router = build_login_router(
    login_request=login_user,
    get_db=get_db,
    required_password_change_request=change_required_password,
)


__all__ = [
    "change_required_password",
    "login_user",
    "password_authentication",
    "router",
]
