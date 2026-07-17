"""Runtime composition for the RFC 8693 token-exchange carrier."""

from tigrbl import TigrblApp
from tigrbl_auth_router_oauth_token_exchange import (
    build_token_exchange_router,
    include_token_exchange_endpoint as include_token_exchange_carrier,
)
from tigrbl_identity_runtime.settings import settings

from .token_exchange_runtime import token_exchange


router = build_token_exchange_router(token_exchange_request=token_exchange)
api = router


def include_token_exchange_endpoint(app: TigrblApp) -> None:
    include_token_exchange_carrier(
        app,
        router,
        enabled=bool(settings.enable_rfc8693),
    )


include_rfc8693 = include_token_exchange_endpoint


__all__ = [
    "api",
    "include_rfc8693",
    "include_token_exchange_endpoint",
    "router",
    "token_exchange",
]
