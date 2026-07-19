import pytest
from tigrbl_identity_protocol_did_core import CURRENT_VERSION, validate_document

def test_did_core_document_relationships_resolve() -> None:
    document = {"id": "did:example:123", "verificationMethod": [{"id": "did:example:123#key-1"}], "authentication": ["did:example:123#key-1"]}
    validate_document(document)
    assert CURRENT_VERSION.identifier == "DID-Core-1.0"

def test_did_core_rejects_unresolved_relationships() -> None:
    with pytest.raises(ValueError): validate_document({"id": "did:example:123", "authentication": ["did:example:123#missing"]})