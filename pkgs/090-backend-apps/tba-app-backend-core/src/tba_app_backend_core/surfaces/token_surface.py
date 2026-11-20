"""Runtime composition for the OAuth token endpoint HTTP carrier."""

from tba_router_oauth_token import build_token_router
from tba_runtime_identity_storage.engine import get_db

from tba_server_identity.token_request import token_request


router = build_token_router(token_request=token_request, get_db=get_db)


__all__ = ["router", "token_request"]
