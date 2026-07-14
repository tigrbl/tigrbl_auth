"""Runtime composition for durable token introspection."""

from __future__ import annotations

from tigrbl_auth_protocol_oauth.standards.rfc7662 import (
    RFC7662IntrospectionService,
)
from tigrbl_identity_storage_runtime.token_lifecycle import introspect_token_async
from tigrbl_token_introspection_capability import TokenIntrospectionCapability


token_introspection = TokenIntrospectionCapability(introspect_token_async)


def build_rfc7662_introspection_service(
    settings_obj: object,
) -> RFC7662IntrospectionService:
    """Bind deployment feature state to the composed introspection capability."""

    return RFC7662IntrospectionService(
        token_introspection,
        enabled=bool(getattr(settings_obj, "enable_rfc7662", False)),
    )


__all__ = [
    "build_rfc7662_introspection_service",
    "token_introspection",
]
