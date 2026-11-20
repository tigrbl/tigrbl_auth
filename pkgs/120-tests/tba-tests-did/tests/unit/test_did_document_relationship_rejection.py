import json
import pytest
from tba_protocol_identity_did_core import DidCoreProtocol


def test_did_document_rejects_unresolved_verification_relationship() -> None:
    document = {
        "id": "did:example:123",
        "verificationMethod": [],
        "authentication": ["did:example:123#missing"],
    }
    with pytest.raises(ValueError, match="unresolved verification relationship"):
        DidCoreProtocol().parse(json.dumps(document))
