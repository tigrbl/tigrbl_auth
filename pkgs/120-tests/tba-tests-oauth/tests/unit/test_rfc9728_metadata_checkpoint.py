from tba_protocol_oauth.standards.protected_resource_metadata import (
    build_protected_resource_metadata,
)
from tba_runtime_identity.deployment import resolve_deployment
from tba_runtime_identity.settings import settings


def test_rfc9728_metadata_has_authorization_server():
    metadata = build_protected_resource_metadata(resolve_deployment(settings))
    assert "authorization_servers" in metadata
    assert metadata["authorization_servers"]
