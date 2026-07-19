import json

from tigrbl_did_document_concrete import DidDocument
from tigrbl_identity_document_contracts import IdentityDocumentVerificationRequest
from tigrbl_identity_protocol_did_core import DidCoreProtocol


DOCUMENT = {
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
}


class _Resolver:
    def resolve(self, identifier: str, /):
        assert identifier == DOCUMENT["id"]
        return DidDocument(identifier, DOCUMENT)


def test_did_core_owns_canonical_document_parsing_and_verification() -> None:
    protocol = DidCoreProtocol()
    document = protocol.parse(json.dumps(DOCUMENT))
    result = protocol.verify(
        IdentityDocumentVerificationRequest(
            document,
            expected_subject=DOCUMENT["id"],
            expected_controller=DOCUMENT["id"],
        )
    )
    assert result.valid and result.key_material_valid and result.representation_valid


def test_did_core_resolution_revalidates_resolved_document() -> None:
    document = DidCoreProtocol(_Resolver()).resolve(DOCUMENT["id"])
    assert document.content["authentication"] == ["did:example:123#key-1"]
