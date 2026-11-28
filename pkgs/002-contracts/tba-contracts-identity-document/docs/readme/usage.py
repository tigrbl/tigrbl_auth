from tba_contracts_identity_document import IdentityDocument

doc = IdentityDocument(
    document_id="did:example:alice",
    subject="did:example:alice",
    kind="did-document",
    representation='{"id":"did:example:alice"}',
    media_type="application/did+json",
)
assert doc.kind.value == "did-document"
