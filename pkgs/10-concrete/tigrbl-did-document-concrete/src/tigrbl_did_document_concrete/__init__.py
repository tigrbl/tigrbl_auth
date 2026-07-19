"""Standalone DID document artifact."""
import json
from typing import Mapping
from tigrbl_identity_core import IdentityDocumentKind
from tigrbl_identity_document_contracts import IdentityDocument

class DidDocument(IdentityDocument):
    def __init__(self, identifier: str, content: Mapping[str, object], *, media_type: str="application/did+json", version: str|None=None, metadata: Mapping[str, object]|None=None):
        if content.get("id") != identifier: raise ValueError("DID document id must match its identifier")
        representation=json.dumps(dict(content),separators=(",",":"),sort_keys=True)
        super().__init__(identifier,identifier,IdentityDocumentKind.DID_DOCUMENT,representation,media_type,identifier,version,metadata or {})
    @property
    def content(self) -> Mapping[str, object]: return json.loads(self.representation)

__all__=["DidDocument"]