"""Runtime composition for the OAuth/OIDC authorization HTTP carrier."""

from tigrbl_auth_router_oauth_authorization import build_authorization_router
from tigrbl_identity_storage_runtime.engine import get_db

from .authorization_runtime import authorize_request


router = build_authorization_router(
    authorize_request=authorize_request,
    get_db=get_db,
)


__all__ = ["authorize_request", "router"]
