"""OAuth/OIDC authorization endpoint HTTP carrier."""

from .binding import (
    AuthorizationRequestTarget,
    DatabaseDependency,
    build_authorization_router,
    include_authorization_endpoint,
)

__all__ = [
    "AuthorizationRequestTarget",
    "DatabaseDependency",
    "build_authorization_router",
    "include_authorization_endpoint",
]
