"""Runtime composition for the interactive session-login HTTP carrier."""

from tigrbl_auth_router_session_login import build_login_router
from tigrbl_identity_storage_runtime.engine import get_db

from tigrbl_identity_server.login_runtime import login_user, password_authentication


router = build_login_router(login_request=login_user, get_db=get_db)


__all__ = ["login_user", "password_authentication", "router"]
