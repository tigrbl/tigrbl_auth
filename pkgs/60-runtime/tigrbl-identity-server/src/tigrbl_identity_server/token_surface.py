"""Runtime composition for the OAuth token endpoint HTTP carrier."""

from tigrbl_auth_api_oauth_token import build_token_router
from tigrbl_identity_storage_runtime.engine import get_db

from .token_request import token_request


router = build_token_router(token_request=token_request, get_db=get_db)


__all__ = ["router", "token_request"]
