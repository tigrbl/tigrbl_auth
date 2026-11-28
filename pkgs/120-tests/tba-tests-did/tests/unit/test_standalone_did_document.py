from tba_concrete_did_document import DidDocument


def test_did_document_is_an_identity_document_not_a_credential() -> None:
    document = DidDocument(
        "did:example:123", {"id": "did:example:123", "verificationMethod": []}
    )
    assert document.subject == "did:example:123"
    assert document.content["id"] == "did:example:123"
    assert not hasattr(document, "format_identifier")
