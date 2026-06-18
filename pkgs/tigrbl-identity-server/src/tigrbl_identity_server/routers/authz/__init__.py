from tigrbl_identity_server.framework import TigrblRouter
from tigrbl_identity_server.rest.routers.authorize import api as authorize_api
from tigrbl_auth_protocol_oauth.standards import rfc6749_token
from tigrbl_auth_protocol_oauth.standards.introspection import api as introspection_api

api = TigrblRouter()
api.include_router(authorize_api)
api.include_router(rfc6749_token.api)
api.include_router(introspection_api)

router = api

__all__ = ["api", "router"]
