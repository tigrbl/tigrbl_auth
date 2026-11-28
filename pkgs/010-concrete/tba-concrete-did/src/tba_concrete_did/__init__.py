from .dereferencing import select_document_resource
from .documents import parse_did_document
from .identifiers import parse_did
from .urls import parse_did_url
from .validation import validate_did_document

__all__ = [
    "parse_did",
    "parse_did_document",
    "parse_did_url",
    "select_document_resource",
    "validate_did_document",
]
