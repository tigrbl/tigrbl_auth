from tigrbl_auth.framework import TigrblRouter
from tigrbl_auth.standards.oauth2 import rfc6749_token
from tigrbl_auth.standards.oauth2.introspection import api as introspection_api

api = TigrblRouter()
api.include_router(rfc6749_token.api)
api.include_router(introspection_api)

router = api

from . import oidc  # noqa: E402,F401

__all__ = ["api", "router"]
