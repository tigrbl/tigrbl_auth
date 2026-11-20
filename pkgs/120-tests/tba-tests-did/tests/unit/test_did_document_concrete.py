import pytest
from tba_concrete_did import (
    parse_did_document,
    parse_did_url,
    select_document_resource,
    validate_did_document,
)


def test_did_document_parsing_validation_and_dereferencing():
    document = parse_did_document(
        {
            "id": "did:example:123",
            "verificationMethod": [
                {
                    "id": "did:example:123#key-1",
                    "type": "JsonWebKey2020",
                    "controller": "did:example:123",
                    "publicKeyJwk": {"kty": "OKP", "crv": "Ed25519", "x": "abc"},
                }
            ],
            "authentication": ["did:example:123#key-1"],
            "service": [
                {
                    "id": "#messages",
                    "type": "Messaging",
                    "serviceEndpoint": "https://example.org/messages",
                }
            ],
        }
    )
    validate_did_document(document)
    method = select_document_resource(document, parse_did_url("did:example:123#key-1"))
    service = select_document_resource(
        document, parse_did_url("did:example:123#messages")
    )
    assert method.method_type == "JsonWebKey2020"
    assert service.service_types == ("Messaging",)


def test_did_document_rejects_unknown_relationship_reference():
    document = parse_did_document(
        {"id": "did:example:123", "authentication": ["did:example:123#missing"]}
    )
    with pytest.raises(ValueError, match="unknown"):
        validate_did_document(document)
