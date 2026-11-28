"""Runtime composition for the interactive session-login HTTP carrier."""

from tba_router_session_login import build_login_router
from tba_runtime_identity_storage.engine import get_db

from tba_server_identity.login_runtime import (
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
