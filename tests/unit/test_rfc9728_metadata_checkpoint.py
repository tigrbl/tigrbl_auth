from tigrbl_auth_protocol_oauth.standards.protected_resource_metadata import build_protected_resource_metadata


def test_rfc9728_metadata_has_authorization_server():
    metadata = build_protected_resource_metadata()
    assert "authorization_servers" in metadata
    assert metadata["authorization_servers"]
