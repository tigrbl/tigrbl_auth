import pytest
from tigrbl_did_concrete import parse_did, parse_did_document, parse_did_url
from tigrbl_did_controller_provider import DidControllerProvider
from tigrbl_did_resolver_provider import VersionedDidResolverProvider


def _document(key: str = "abc"):
    return parse_did_document(
        {
            "id": "did:example:123",
            "verificationMethod": [
                {
                    "id": "did:example:123#key-1",
                    "type": "JsonWebKey2020",
                    "controller": "did:example:123",
                    "publicKeyJwk": {"kty": "OKP", "crv": "Ed25519", "x": key},
                }
            ],
            "authentication": ["did:example:123#key-1"],
        }
    )


def test_resolver_publishes_versions_resolves_and_dereferences():
    resolver = VersionedDidResolverProvider()
    resolver.publish(_document(), "v1")
    result = resolver.resolve(parse_did("did:example:123"))
    dereferenced = resolver.dereference(parse_did_url("did:example:123#key-1"))
    assert result.document_metadata["versionId"] == "v1"
    assert dereferenced.content.method_type == "JsonWebKey2020"


def test_resolver_reports_method_not_supported_without_implying_trust():
    result = VersionedDidResolverProvider().resolve(parse_did("did:unknown:123"))
    assert result.document is None
    assert result.resolution_metadata["error"] == "methodNotSupported"
    assert "trusted" not in result.resolution_metadata


def test_method_resolver_validates_returned_document_identifier():
    resolver = VersionedDidResolverProvider()
    resolver.register_method("example", lambda did: _document())
    result = resolver.resolve(parse_did("did:example:different"))
    assert result.document is None
    assert result.resolution_metadata["error"] == "invalidDidDocument"


def test_controller_requires_control_proof_before_publishing_version():
    resolver = VersionedDidResolverProvider()
    controller = DidControllerProvider(
        lambda current, proposed, proof: proof == "authorized",
        resolver.publish,
    )
    with pytest.raises(PermissionError):
        controller.apply(_document(), "v1", "bad-proof")
    created = controller.apply(_document(), "v1", "authorized")
    updated = controller.apply(_document("updated"), "v2", "authorized")
    assert created.created and not updated.created
    assert (
        resolver.resolve(parse_did("did:example:123")).document_metadata["versionId"]
        == "v2"
    )
