"""Owned mapped-table inventory."""

from .did_gnap_state import DidDocument, DidDocumentVersion, DidVerificationMethod, DidService, DidResolutionCache

TABLE_MODELS = (
    DidDocument,
    DidDocumentVersion,
    DidVerificationMethod,
    DidService,
    DidResolutionCache,
)
TABLE_MODEL_BY_NAME = {model.__name__: model for model in TABLE_MODELS}
TABLE_MODEL_BY_TABLENAME = {model.__tablename__: model for model in TABLE_MODELS}
__all__ = [model.__name__ for model in TABLE_MODELS] + [
    "TABLE_MODELS", "TABLE_MODEL_BY_NAME", "TABLE_MODEL_BY_TABLENAME",
]
