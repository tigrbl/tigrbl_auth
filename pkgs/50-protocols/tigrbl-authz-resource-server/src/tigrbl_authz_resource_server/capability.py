"""Composition of a resource-server provider into its layer-40 capability."""

from tigrbl_authz_resource_server_verifier import ResourceServerVerifier
from tigrbl_identity_contracts.resource_server import ResourceServerVerifierPort
from tigrbl_protected_resource_authorization_capability import (
    ProtectedResourceAuthorizationCapability,
)


def build_protected_resource_authorization_capability(
    verifier: ResourceServerVerifierPort | None = None,
) -> ProtectedResourceAuthorizationCapability:
    return ProtectedResourceAuthorizationCapability(
        verifier if verifier is not None else ResourceServerVerifier()
    )


__all__ = [
    "ProtectedResourceAuthorizationCapability",
    "build_protected_resource_authorization_capability",
]
