"""Runtime composition for durable token introspection."""

from __future__ import annotations

from tba_protocol_oauth.standards.introspection import (
    RFC7662IntrospectionService,
)
from tba_runtime_identity_storage.token_lifecycle import introspect_token_async
from tba_capability_token_introspection import TokenIntrospectionCapability


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
