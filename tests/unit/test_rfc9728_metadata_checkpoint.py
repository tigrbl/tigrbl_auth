from tigrbl_auth_protocol_oauth.standards.protected_resource_metadata import (
    build_protected_resource_metadata,
)
from tigrbl_identity_runtime.deployment import resolve_deployment
from tigrbl_identity_runtime.settings import settings


def test_rfc9728_metadata_has_authorization_server():
    metadata = build_protected_resource_metadata(resolve_deployment(settings))
    assert "authorization_servers" in metadata
    assert metadata["authorization_servers"]
