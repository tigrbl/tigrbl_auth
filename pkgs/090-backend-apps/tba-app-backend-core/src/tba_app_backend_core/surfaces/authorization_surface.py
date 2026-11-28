"""Runtime composition for the OAuth/OIDC authorization HTTP carrier."""

from tba_router_oauth_authorization import build_authorization_router
from tba_runtime_identity_storage.engine import get_db

from tba_server_identity.authorization_runtime import authorize_request


router = build_authorization_router(
    authorize_request=authorize_request,
    get_db=get_db,
)


__all__ = ["authorize_request", "router"]
